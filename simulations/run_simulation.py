"""
Simulation runner for L2/3 barrel cortex network.

Provides functions to run simulations with different protocols:
- Spontaneous activity
- Sensory input stimulation
- Current injection
- Optogenetic stimulation

Author: NeuroV2 Project
Date: 2025
"""

import numpy as np
from neuron import h
import time
from typing import Dict, List, Optional
import sys
sys.path.append('..')


class SimulationRunner:
    """Run simulations on L2/3 network."""

    def __init__(self, network, dt: float = 0.025, celsius: float = 34.0):
        """
        Initialize simulation runner.

        Parameters
        ----------
        network : L23Network
            Network to simulate
        dt : float
            Time step (ms)
        celsius : float
            Temperature (deg C)
        """
        self.network = network
        self.dt = dt
        self.celsius = celsius

        # Setup NEURON simulation parameters
        h.load_file("stdrun.hoc")
        h.dt = dt
        h.celsius = celsius
        h.v_init = -70

        # Recording vectors
        self.t_vec = h.Vector()
        self.t_vec.record(h._ref_t)

        # Spike times for each cell
        self.spike_times = {}
        for cell in network.cells:
            self.spike_times[cell.gid] = cell.spike_times

        print(f"Simulation initialized: dt={dt} ms, T={celsius} C")

    def run(self, duration: float, progress_interval: float = 100.0):
        """
        Run simulation for specified duration.

        Parameters
        ----------
        duration : float
            Simulation duration (ms)
        progress_interval : float
            Print progress every N ms
        """
        print(f"\nRunning simulation for {duration} ms...")

        h.finitialize(h.v_init)
        h.fcurrent()

        start_time = time.time()
        last_print = 0

        while h.t < duration:
            h.fadvance()

            # Progress update
            if h.t - last_print >= progress_interval:
                percent = 100 * h.t / duration
                print(f"  Progress: {h.t:.1f}/{duration} ms ({percent:.1f}%)")
                last_print = h.t

        elapsed = time.time() - start_time
        print(f"Simulation completed in {elapsed:.2f} seconds")
        print(f"  Simulated time: {duration} ms")
        print(f"  Real-time ratio: {duration / (elapsed * 1000):.2f}x")

    def run_baseline(self, duration: float = 1000.0):
        """
        Run baseline spontaneous activity simulation.

        Parameters
        ----------
        duration : float
            Duration (ms)
        """
        print("\n=== Running Baseline Simulation ===")
        self.run(duration)
        self._analyze_spikes()

    def add_background_input(
        self,
        rate: float = 5.0,
        weight: float = 0.0005,
        start: float = 0,
        duration: float = None,
    ):
        """
        Add Poisson background input to all cells.

        Parameters
        ----------
        rate : float
            Mean firing rate (Hz)
        weight : float
            Synaptic weight (uS)
        start : float
            Start time (ms)
        duration : float
            Duration (ms), None for entire simulation
        """
        print(f"\nAdding background input: {rate} Hz")

        self.background_stims = []

        for cell in self.network.cells:
            # Add AMPA synapse to soma
            syn = cell.add_synapse("AMPA", cell.soma, location=0.5, gmax=weight)

            # Create NetStim (Poisson process)
            stim = h.NetStim()
            stim.interval = 1000.0 / rate  # ms
            stim.number = 1e9  # Effectively infinite
            stim.start = start
            stim.noise = 1  # Poisson

            # Connect to synapse
            nc = h.NetCon(stim, syn)
            nc.weight[0] = 1.0
            nc.delay = 0.1

            self.background_stims.append((stim, nc, syn))

    def stimulate_cells(
        self,
        cell_indices: List[int],
        start: float = 100.0,
        duration: float = 500.0,
        rate: float = 20.0,
        weight: float = 0.001,
    ):
        """
        Stimulate specific cells with Poisson input.

        Parameters
        ----------
        cell_indices : list
            Indices of cells to stimulate
        start : float
            Start time (ms)
        duration : float
            Duration (ms)
        rate : float
            Stimulation rate (Hz)
        weight : float
            Synaptic weight (uS)
        """
        print(f"\nStimulating {len(cell_indices)} cells")
        print(f"  Start: {start} ms, Duration: {duration} ms, Rate: {rate} Hz")

        self.stim_inputs = []

        for idx in cell_indices:
            cell = self.network.cells[idx]

            # Add AMPA synapse
            syn = cell.add_synapse("AMPA", cell.soma, location=0.5, gmax=weight)

            # Create NetStim
            stim = h.NetStim()
            stim.interval = 1000.0 / rate
            stim.number = int(rate * duration / 1000)
            stim.start = start
            stim.noise = 1

            # Connect
            nc = h.NetCon(stim, syn)
            nc.weight[0] = 1.0
            nc.delay = 0.1

            self.stim_inputs.append((stim, nc, syn))

    def inject_current(
        self,
        cell_index: int,
        amplitude: float,
        start: float = 100.0,
        duration: float = 500.0,
    ):
        """
        Inject current into a cell.

        Parameters
        ----------
        cell_index : int
            Index of cell
        amplitude : float
            Current amplitude (nA)
        start : float
            Start time (ms)
        duration : float
            Duration (ms)
        """
        cell = self.network.cells[cell_index]

        iclamp = h.IClamp(cell.soma(0.5))
        iclamp.delay = start
        iclamp.dur = duration
        iclamp.amp = amplitude

        print(f"Injecting {amplitude} nA into cell {cell_index}")

        # Store to prevent garbage collection
        if not hasattr(self, 'current_clamps'):
            self.current_clamps = []
        self.current_clamps.append(iclamp)

    def _analyze_spikes(self):
        """Analyze and print spike statistics."""
        print("\n=== Spike Statistics ===")

        total_spikes = 0
        active_cells = 0

        spike_counts_by_type = {}

        for cell in self.network.cells:
            n_spikes = len(cell.spike_times)
            total_spikes += n_spikes

            if n_spikes > 0:
                active_cells += 1

            cell_type = cell.cell_type
            if cell_type not in spike_counts_by_type:
                spike_counts_by_type[cell_type] = []
            spike_counts_by_type[cell_type].append(n_spikes)

        print(f"Total spikes: {total_spikes}")
        print(f"Active cells: {active_cells}/{len(self.network.cells)}")
        print(f"Mean rate: {total_spikes / len(self.network.cells):.2f} spikes/cell")

        print("\nBy cell type:")
        for cell_type, counts in sorted(spike_counts_by_type.items()):
            mean_count = np.mean(counts)
            std_count = np.std(counts)
            print(f"  {cell_type}: {mean_count:.2f} ± {std_count:.2f} spikes/cell")

    def save_results(self, filename: str):
        """Save simulation results to file."""
        import h5py

        print(f"\nSaving results to {filename}")

        with h5py.File(filename, 'w') as f:
            # Time vector
            f.create_dataset('time', data=np.array(self.t_vec))

            # Spike times
            spikes_group = f.create_group('spikes')
            for cell in self.network.cells:
                gid = cell.gid
                spikes = np.array(cell.spike_times)
                spikes_group.create_dataset(str(gid), data=spikes)

            # Metadata
            f.attrs['n_cells'] = len(self.network.cells)
            f.attrs['duration'] = self.t_vec[-1]
            f.attrs['dt'] = self.dt
            f.attrs['celsius'] = self.celsius

        print("Results saved successfully")


def run_baseline_simulation(
    network,
    duration: float = 1000.0,
    background_rate: float = 5.0,
    output_file: Optional[str] = None,
):
    """
    Run baseline spontaneous activity simulation.

    Parameters
    ----------
    network : L23Network
        Network to simulate
    duration : float
        Simulation duration (ms)
    background_rate : float
        Background Poisson input rate (Hz)
    output_file : str, optional
        HDF5 file to save results

    Returns
    -------
    runner : SimulationRunner
        Simulation runner with results
    """
    runner = SimulationRunner(network)

    # Add background input
    if background_rate > 0:
        runner.add_background_input(rate=background_rate)

    # Run simulation
    runner.run_baseline(duration=duration)

    # Save results
    if output_file:
        runner.save_results(output_file)

    return runner


def main():
    """Main function for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Run L2/3 barrel cortex simulation")
    parser.add_argument("--n-cells", type=int, default=2000, help="Number of cells")
    parser.add_argument("--duration", type=float, default=1000, help="Duration (ms)")
    parser.add_argument(
        "--background-rate", type=float, default=5.0, help="Background rate (Hz)"
    )
    parser.add_argument("--output", type=str, help="Output HDF5 file")
    parser.add_argument("--seed", type=int, default=12345, help="Random seed")

    args = parser.parse_args()

    # Build network
    from network.build_network import build_l23_network

    network = build_l23_network(n_cells=args.n_cells, seed=args.seed)

    # Run simulation
    runner = run_baseline_simulation(
        network,
        duration=args.duration,
        background_rate=args.background_rate,
        output_file=args.output,
    )

    print("\nSimulation complete!")


if __name__ == "__main__":
    main()
