"""
Basic analysis tools for L2/3 simulation results.

Functions for analyzing:
- Spike raster plots
- Firing rate distributions
- Population activity
- Network synchrony

Author: NeuroV2 Project
Date: 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import h5py
from typing import Dict, List, Tuple


def load_results(filename: str) -> Dict:
    """
    Load simulation results from HDF5 file.

    Parameters
    ----------
    filename : str
        Path to HDF5 file

    Returns
    -------
    results : dict
        Dictionary containing spike times and metadata
    """
    results = {}

    with h5py.File(filename, 'r') as f:
        # Load time
        results['time'] = np.array(f['time'])

        # Load spikes
        results['spikes'] = {}
        for gid in f['spikes'].keys():
            results['spikes'][int(gid)] = np.array(f['spikes'][gid])

        # Load metadata
        results['n_cells'] = f.attrs['n_cells']
        results['duration'] = f.attrs['duration']
        results['dt'] = f.attrs['dt']

    return results


def plot_raster(
    spike_times: Dict[int, np.ndarray],
    cell_types: List[str] = None,
    figsize: Tuple[float, float] = (12, 6),
    save_path: str = None,
):
    """
    Plot spike raster.

    Parameters
    ----------
    spike_times : dict
        Dictionary mapping cell GID to spike times
    cell_types : list, optional
        List of cell types for coloring
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Color map for cell types
    type_colors = {
        'L23_Pyramidal': 'black',
        'PV_Basket': 'red',
        'SST_Martinotti': 'blue',
        'VIP_Interneuron': 'green',
    }

    for gid, times in spike_times.items():
        if len(times) > 0:
            color = 'black'
            if cell_types and gid < len(cell_types):
                color = type_colors.get(cell_types[gid], 'black')

            ax.scatter(times, [gid] * len(times), c=color, s=1, marker='|')

    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Cell ID', fontsize=12)
    ax.set_title('Spike Raster Plot', fontsize=14)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Raster plot saved to {save_path}")

    plt.show()


def plot_firing_rates(
    spike_times: Dict[int, np.ndarray],
    duration: float,
    cell_types: List[str] = None,
    figsize: Tuple[float, float] = (10, 6),
    save_path: str = None,
):
    """
    Plot firing rate distribution.

    Parameters
    ----------
    spike_times : dict
        Dictionary mapping cell GID to spike times
    duration : float
        Simulation duration (ms)
    cell_types : list, optional
        List of cell types
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    # Calculate firing rates
    rates = {}
    for gid, times in spike_times.items():
        rates[gid] = len(times) / (duration / 1000.0)  # Hz

    # Group by cell type if provided
    if cell_types:
        rates_by_type = {}
        for gid, rate in rates.items():
            if gid < len(cell_types):
                cell_type = cell_types[gid]
                if cell_type not in rates_by_type:
                    rates_by_type[cell_type] = []
                rates_by_type[cell_type].append(rate)

        # Plot distributions
        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Histogram
        for cell_type, type_rates in rates_by_type.items():
            axes[0].hist(
                type_rates, bins=20, alpha=0.6, label=cell_type.replace('_', ' ')
            )

        axes[0].set_xlabel('Firing Rate (Hz)', fontsize=12)
        axes[0].set_ylabel('Count', fontsize=12)
        axes[0].set_title('Firing Rate Distribution', fontsize=14)
        axes[0].legend()

        # Box plot
        type_names = list(rates_by_type.keys())
        type_data = [rates_by_type[t] for t in type_names]
        axes[1].boxplot(type_data, labels=[t.replace('_', '\n') for t in type_names])
        axes[1].set_ylabel('Firing Rate (Hz)', fontsize=12)
        axes[1].set_title('Firing Rates by Cell Type', fontsize=14)
        axes[1].tick_params(axis='x', rotation=0)

        plt.tight_layout()
    else:
        # Simple histogram
        fig, ax = plt.subplots(figsize=figsize)
        ax.hist(list(rates.values()), bins=30)
        ax.set_xlabel('Firing Rate (Hz)', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title('Firing Rate Distribution', fontsize=14)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Firing rate plot saved to {save_path}")

    plt.show()


def plot_population_rate(
    spike_times: Dict[int, np.ndarray],
    duration: float,
    bin_size: float = 10.0,
    figsize: Tuple[float, float] = (12, 4),
    save_path: str = None,
):
    """
    Plot population firing rate over time.

    Parameters
    ----------
    spike_times : dict
        Dictionary mapping cell GID to spike times
    duration : float
        Simulation duration (ms)
    bin_size : float
        Time bin size (ms)
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save figure
    """
    # Bin spikes
    bins = np.arange(0, duration + bin_size, bin_size)
    pop_rate = np.zeros(len(bins) - 1)

    for times in spike_times.values():
        if len(times) > 0:
            counts, _ = np.histogram(times, bins=bins)
            pop_rate += counts

    # Convert to rate (Hz)
    pop_rate = pop_rate / (bin_size / 1000.0) / len(spike_times)

    # Plot
    fig, ax = plt.subplots(figsize=figsize)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    ax.plot(bin_centers, pop_rate, 'k-', linewidth=1)
    ax.fill_between(bin_centers, pop_rate, alpha=0.3)

    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_ylabel('Population Rate (Hz)', fontsize=12)
    ax.set_title(f'Population Firing Rate (bin={bin_size} ms)', fontsize=14)
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Population rate plot saved to {save_path}")

    plt.show()


def calculate_synchrony(
    spike_times: Dict[int, np.ndarray],
    duration: float,
    bin_size: float = 5.0,
) -> float:
    """
    Calculate network synchrony using spike count correlation.

    Parameters
    ----------
    spike_times : dict
        Dictionary mapping cell GID to spike times
    duration : float
        Simulation duration (ms)
    bin_size : float
        Time bin size (ms)

    Returns
    -------
    synchrony : float
        Synchrony measure (0 to 1)
    """
    bins = np.arange(0, duration + bin_size, bin_size)
    n_cells = len(spike_times)

    # Create spike count matrix
    spike_counts = np.zeros((n_cells, len(bins) - 1))

    for i, times in enumerate(spike_times.values()):
        if len(times) > 0:
            counts, _ = np.histogram(times, bins=bins)
            spike_counts[i, :] = counts

    # Calculate pairwise correlations
    correlations = np.corrcoef(spike_counts)

    # Remove diagonal and NaNs
    mask = ~np.eye(n_cells, dtype=bool)
    correlations = correlations[mask]
    correlations = correlations[~np.isnan(correlations)]

    if len(correlations) == 0:
        return 0.0

    # Mean correlation as synchrony measure
    synchrony = np.mean(correlations)

    return max(0, synchrony)  # Clip negative values


def print_summary_statistics(results: Dict):
    """
    Print summary statistics of simulation results.

    Parameters
    ----------
    results : dict
        Results dictionary from load_results()
    """
    spike_times = results['spikes']
    duration = results['duration']
    n_cells = results['n_cells']

    print("\n=== Summary Statistics ===")
    print(f"Duration: {duration:.1f} ms")
    print(f"Number of cells: {n_cells}")

    # Total spikes
    total_spikes = sum(len(times) for times in spike_times.values())
    print(f"Total spikes: {total_spikes}")

    # Active cells
    active_cells = sum(1 for times in spike_times.values() if len(times) > 0)
    print(f"Active cells: {active_cells}/{n_cells} ({100*active_cells/n_cells:.1f}%)")

    # Firing rates
    rates = [len(times) / (duration / 1000.0) for times in spike_times.values()]
    print(f"Mean firing rate: {np.mean(rates):.2f} ± {np.std(rates):.2f} Hz")
    print(f"Median firing rate: {np.median(rates):.2f} Hz")

    # Synchrony
    sync = calculate_synchrony(spike_times, duration)
    print(f"Network synchrony: {sync:.3f}")


def main():
    """Example usage."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python basic_analysis.py <results.h5>")
        return

    filename = sys.argv[1]

    # Load results
    print(f"Loading {filename}...")
    results = load_results(filename)

    # Print statistics
    print_summary_statistics(results)

    # Create plots
    print("\nGenerating plots...")
    plot_raster(results['spikes'])
    plot_firing_rates(results['spikes'], results['duration'])
    plot_population_rate(results['spikes'], results['duration'])


if __name__ == "__main__":
    main()
