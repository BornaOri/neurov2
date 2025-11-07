"""
Base cell class for all neuron types in the L2/3 barrel cortex simulation.

Provides common functionality for morphology loading, channel insertion,
and basic electrophysiology.

Author: NeuroV2 Project
Date: 2025
"""

from neuron import h
import numpy as np
from typing import Dict, List, Optional, Tuple


class BaseCell:
    """Base class for all neuron models."""

    def __init__(
        self,
        gid: int,
        cell_type: str,
        morphology_file: Optional[str] = None,
        position: Optional[Tuple[float, float, float]] = None,
    ):
        """
        Initialize base cell.

        Parameters
        ----------
        gid : int
            Global identifier for this cell
        cell_type : str
            Type of cell (e.g., 'pyramidal', 'basket', 'martinotti')
        morphology_file : str, optional
            Path to SWC or ASC morphology file
        position : tuple, optional
            3D position (x, y, z) in microns
        """
        self.gid = gid
        self.cell_type = cell_type
        self.morphology_file = morphology_file
        self.position = position if position else (0.0, 0.0, 0.0)

        # NEURON structures
        self.soma = None
        self.dends = []
        self.apic = []  # apical dendrites (for pyramidal cells)
        self.axon = []
        self.all_sections = []

        # Synapses
        self.synapses = {
            "AMPA": [],
            "NMDA": [],
            "GABAA": [],
            "GABAB": [],
        }
        self.netcons = []

        # Recording vectors
        self.spike_detector = None
        self.spike_times = h.Vector()

        # Biophysical parameters (to be set by subclasses)
        self.biophys_params = {}

    def create_morphology(self):
        """Create or load cell morphology. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement create_morphology()")

    def insert_channels(self):
        """Insert ion channels into sections. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement insert_channels()")

    def define_biophysics(self):
        """Define biophysical properties. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement define_biophysics()")

    def set_position(self, x: float, y: float, z: float):
        """Set 3D position of the cell."""
        self.position = (x, y, z)
        for sec in self.all_sections:
            for i in range(sec.n3d()):
                h.pt3dchange(
                    i,
                    x + sec.x3d(i),
                    y + sec.y3d(i),
                    z + sec.z3d(i),
                    sec.diam3d(i),
                    sec=sec,
                )

    def setup_spike_detection(self, threshold: float = -20.0):
        """
        Setup spike detection at soma.

        Parameters
        ----------
        threshold : float
            Voltage threshold for spike detection (mV)
        """
        self.spike_detector = h.NetCon(
            self.soma(0.5)._ref_v, None, sec=self.soma
        )
        self.spike_detector.threshold = threshold
        self.spike_detector.record(self.spike_times)

    def add_synapse(
        self,
        syn_type: str,
        section,
        location: float = 0.5,
        **params
    ) -> object:
        """
        Add a synapse to the cell.

        Parameters
        ----------
        syn_type : str
            Type of synapse ('AMPA', 'NMDA', 'GABAA', 'GABAB')
        section : h.Section
            Section to place synapse on
        location : float
            Location along section (0 to 1)
        **params : dict
            Additional synapse parameters

        Returns
        -------
        synapse : NEURON point process
            The created synapse object
        """
        if syn_type not in self.synapses:
            raise ValueError(f"Unknown synapse type: {syn_type}")

        # Create synapse
        if syn_type == "AMPA":
            syn = h.AMPA(section(location))
        elif syn_type == "NMDA":
            syn = h.NMDA(section(location))
        elif syn_type == "GABAA":
            syn = h.GABAA(section(location))
        elif syn_type == "GABAB":
            syn = h.GABAB(section(location))

        # Set parameters
        for param, value in params.items():
            if hasattr(syn, param):
                setattr(syn, param, value)

        # Store synapse
        self.synapses[syn_type].append(syn)

        return syn

    def get_section_by_name(self, name: str):
        """Get section by name."""
        for sec in self.all_sections:
            if sec.name().endswith(name):
                return sec
        return None

    def get_compartment_area(self, section) -> float:
        """Calculate surface area of a section in um2."""
        area = 0
        for seg in section:
            area += seg.area()
        return area

    def print_info(self):
        """Print cell information."""
        print(f"Cell {self.gid} ({self.cell_type})")
        print(f"  Position: {self.position}")
        print(f"  Sections: {len(self.all_sections)}")
        print(f"  Synapses: {sum(len(v) for v in self.synapses.values())}")
        if self.morphology_file:
            print(f"  Morphology: {self.morphology_file}")

    def __repr__(self):
        return f"{self.__class__.__name__}(gid={self.gid}, type={self.cell_type})"
