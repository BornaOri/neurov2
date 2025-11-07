"""
Network building functions for L2/3 barrel cortex simulation.

Creates biologically realistic networks with:
- Realistic cell type proportions
- Distance-dependent connectivity
- Multiple synapses per connection
- Biophysically constrained weights and delays

Author: NeuroV2 Project
Date: 2025
"""

import numpy as np
from neuron import h
from typing import List, Dict, Tuple
import sys
sys.path.append('..')

from cells import create_cell, CELL_TYPE_PROPORTIONS
from parameters.connectivity_params import (
    get_connection_probability,
    get_synaptic_parameters,
    distance_dependent_probability,
    SYNAPSES_PER_CONNECTION,
    SYNAPTIC_DELAYS,
    CONNECTION_PROBABILITIES,
)


class L23Network:
    """L2/3 barrel cortex network."""

    def __init__(
        self,
        n_cells: int = 2000,
        volume: Tuple[float, float, float] = (400, 400, 300),
        seed: int = 12345,
    ):
        """
        Initialize network.

        Parameters
        ----------
        n_cells : int
            Total number of cells in network
        volume : tuple
            Network volume (x, y, z) in microns
        seed : int
            Random seed for reproducibility
        """
        self.n_cells = n_cells
        self.volume = volume
        self.seed = seed

        np.random.seed(seed)

        # Network components
        self.cells = []
        self.cell_positions = []
        self.cell_types = []
        self.connections = []  # List of (pre_gid, post_gid, syn_list)
        self.netcons = []

        print(f"Initializing L2/3 network with {n_cells} cells")
        print(f"Volume: {volume} um^3")

    def create_cells(self):
        """Create all cells with realistic proportions."""
        print("\nCreating cells...")

        # Determine number of each cell type
        cell_type_counts = self._get_cell_type_counts()

        gid = 0
        for cell_type, count in cell_type_counts.items():
            if cell_type == "Other_Inhibitory":
                continue  # Skip for now, or implement other IN types

            print(f"  Creating {count} {cell_type} cells...")

            for i in range(count):
                # Random position in volume
                pos = self._generate_position()

                # Create cell
                cell = create_cell(gid=gid, cell_type=cell_type, position=pos)

                self.cells.append(cell)
                self.cell_positions.append(pos)
                self.cell_types.append(cell_type)

                gid += 1

        print(f"Created {len(self.cells)} cells")
        self._print_cell_type_summary()

    def _get_cell_type_counts(self) -> Dict[str, int]:
        """Calculate number of cells of each type."""
        counts = {}
        remaining = self.n_cells

        # Allocate cells proportionally
        for cell_type, proportion in CELL_TYPE_PROPORTIONS.items():
            if cell_type == "Other_Inhibitory":
                continue

            count = int(np.round(self.n_cells * proportion))
            counts[cell_type] = count
            remaining -= count

        # Distribute remaining cells to pyramidal
        if remaining > 0:
            counts["L23_Pyramidal"] += remaining

        return counts

    def _generate_position(self) -> Tuple[float, float, float]:
        """Generate random position within volume."""
        x = np.random.uniform(0, self.volume[0])
        y = np.random.uniform(0, self.volume[1])
        z = np.random.uniform(0, self.volume[2])
        return (x, y, z)

    def _print_cell_type_summary(self):
        """Print summary of cell types in network."""
        from collections import Counter

        type_counts = Counter(self.cell_types)
        print("\nCell type distribution:")
        for cell_type, count in sorted(type_counts.items()):
            percentage = 100 * count / len(self.cells)
            print(f"  {cell_type}: {count} ({percentage:.1f}%)")

    def connect_cells(self, use_distance: bool = True):
        """
        Create synaptic connections between cells.

        Parameters
        ----------
        use_distance : bool
            If True, use distance-dependent connectivity
        """
        print("\nConnecting cells...")

        n_connections = 0

        for pre_gid, pre_cell in enumerate(self.cells):
            pre_type = self.cell_types[pre_gid]
            pre_pos = self.cell_positions[pre_gid]

            for post_gid, post_cell in enumerate(self.cells):
                if pre_gid == post_gid:
                    continue  # No autapses

                post_type = self.cell_types[post_gid]
                post_pos = self.cell_positions[post_gid]

                # Get base connection probability
                p_conn = get_connection_probability(pre_type, post_type)

                if p_conn == 0:
                    continue

                # Apply distance dependence
                if use_distance:
                    distance = self._calculate_distance(pre_pos, post_pos)
                    p_dist = distance_dependent_probability(distance, pre_type)
                    p_conn *= p_dist

                # Decide if connection exists
                if np.random.random() < p_conn:
                    # Create connection
                    n_synapses = self._make_connection(
                        pre_cell, post_cell, pre_type, post_type, pre_gid, post_gid
                    )
                    n_connections += 1

            # Progress update
            if (pre_gid + 1) % 100 == 0:
                print(f"  Connected {pre_gid + 1}/{len(self.cells)} cells...")

        print(f"Created {n_connections} connections")
        print(f"Average {n_connections / len(self.cells):.1f} connections per cell")

    def _calculate_distance(
        self, pos1: Tuple[float, float, float], pos2: Tuple[float, float, float]
    ) -> float:
        """Calculate Euclidean distance between two positions."""
        return np.sqrt(
            (pos1[0] - pos2[0]) ** 2
            + (pos1[1] - pos2[1]) ** 2
            + (pos1[2] - pos2[2]) ** 2
        )

    def _make_connection(
        self,
        pre_cell,
        post_cell,
        pre_type: str,
        post_type: str,
        pre_gid: int,
        post_gid: int,
    ) -> int:
        """
        Create synaptic connection between two cells.

        Returns
        -------
        n_synapses : int
            Number of synapses created
        """
        # Determine synapse types based on pre cell
        if "Pyramidal" in pre_type:
            syn_types = ["AMPA", "NMDA"]
        else:
            # Inhibitory
            if "SST" in pre_type and "Pyramidal" in post_type:
                syn_types = ["GABAA", "GABAB"]  # SST has both
            else:
                syn_types = ["GABAA"]

        # Number of synaptic contacts
        key = (pre_type, post_type)
        mean_n, std_n = SYNAPSES_PER_CONNECTION.get(key, (1.0, 0.5))
        n_synapses = max(1, int(np.round(np.random.normal(mean_n, std_n))))

        # Get delay parameters
        delay_mean, delay_std, delay_min, delay_max = SYNAPTIC_DELAYS.get(
            key, (1.5, 0.5, 0.5, 5.0)
        )

        synapses_created = []

        for syn_type in syn_types:
            # Get weight parameters
            weight_mean, weight_std, weight_min, weight_max = get_synaptic_parameters(
                pre_type, post_type, syn_type
            )

            if weight_mean == 0:
                continue

            for i in range(n_synapses):
                # Sample weight
                weight = np.random.normal(weight_mean, weight_std)
                weight = np.clip(weight, weight_min, weight_max)

                # Sample delay
                delay = np.random.normal(delay_mean, delay_std)
                delay = np.clip(delay, delay_min, delay_max)

                # Choose target section and location
                target_sec, target_loc = self._choose_synapse_location(
                    post_cell, post_type, syn_type
                )

                # Create synapse
                syn = post_cell.add_synapse(
                    syn_type=syn_type,
                    section=target_sec,
                    location=target_loc,
                    gmax=weight,
                )

                # Create NetCon
                nc = h.NetCon(
                    pre_cell.spike_detector,
                    syn,
                    sec=pre_cell.soma,
                )
                nc.delay = delay
                nc.weight[0] = 1.0  # Weight is in synapse gmax

                self.netcons.append(nc)
                synapses_created.append(syn)

        self.connections.append((pre_gid, post_gid, synapses_created))

        return len(synapses_created)

    def _choose_synapse_location(self, cell, post_type: str, syn_type: str):
        """
        Choose appropriate section and location for synapse.

        Parameters
        ----------
        cell : BaseCell
            Postsynaptic cell
        post_type : str
            Postsynaptic cell type
        syn_type : str
            Synapse type

        Returns
        -------
        section : h.Section
            Target section
        location : float
            Location along section (0 to 1)
        """
        # For pyramidal cells, choose based on synapse type
        if "Pyramidal" in post_type:
            if syn_type in ["AMPA", "NMDA"]:
                # Excitatory on dendrites
                if cell.apic and np.random.random() < 0.4:
                    section = np.random.choice(cell.apic)
                elif cell.dends:
                    section = np.random.choice(cell.dends)
                else:
                    section = cell.soma
            elif "SST" in syn_type or syn_type == "GABAB":
                # SST targets distal dendrites
                if cell.apic:
                    section = np.random.choice(cell.apic)
                else:
                    section = cell.soma
            else:  # PV GABAA
                # Perisomatic
                if np.random.random() < 0.6:
                    section = cell.soma
                elif cell.dends:
                    section = np.random.choice(cell.dends[:2])  # Proximal
                else:
                    section = cell.soma
        else:
            # For interneurons, use soma and proximal dendrites
            if cell.dends and np.random.random() < 0.5:
                section = np.random.choice(cell.dends)
            else:
                section = cell.soma

        # Random location along section
        location = np.random.uniform(0.2, 0.8)

        return section, location

    def save_network(self, filename: str):
        """Save network structure to file."""
        import pickle

        network_data = {
            "n_cells": self.n_cells,
            "volume": self.volume,
            "seed": self.seed,
            "cell_types": self.cell_types,
            "cell_positions": self.cell_positions,
            "connections": [
                (pre, post, len(syns)) for pre, post, syns in self.connections
            ],
        }

        with open(filename, "wb") as f:
            pickle.dump(network_data, f)

        print(f"Network saved to {filename}")

    def get_connection_stats(self):
        """Print connectivity statistics."""
        from collections import defaultdict

        print("\n=== Connection Statistics ===")

        # Count connections by type
        conn_counts = defaultdict(int)
        for pre_gid, post_gid, syns in self.connections:
            pre_type = self.cell_types[pre_gid]
            post_type = self.cell_types[post_gid]
            key = (pre_type, post_type)
            conn_counts[key] += 1

        print("\nConnections by type pair:")
        for (pre_type, post_type), count in sorted(conn_counts.items()):
            print(f"  {pre_type} -> {post_type}: {count}")


def build_l23_network(
    n_cells: int = 2000,
    volume: Tuple[float, float, float] = (400, 400, 300),
    seed: int = 12345,
) -> L23Network:
    """
    Convenience function to build complete L2/3 network.

    Parameters
    ----------
    n_cells : int
        Number of cells
    volume : tuple
        Network volume (x, y, z) in microns
    seed : int
        Random seed

    Returns
    -------
    network : L23Network
        Constructed network
    """
    network = L23Network(n_cells=n_cells, volume=volume, seed=seed)
    network.create_cells()
    network.connect_cells(use_distance=True)
    network.get_connection_stats()

    return network
