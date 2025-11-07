"""
Parvalbumin-positive Basket Cell

Fast-spiking GABAergic interneuron.
Targets soma and proximal dendrites of pyramidal cells.
Based on Hu et al. (2014) and Markram et al. (2004).

Author: NeuroV2 Project
Date: 2025
"""

from neuron import h
from .base_cell import BaseCell


class PVBasket(BaseCell):
    """Parvalbumin-positive basket cell (fast-spiking interneuron)."""

    def __init__(
        self,
        gid: int,
        morphology_file: str = None,
        position: tuple = None,
    ):
        """
        Initialize PV+ basket cell.

        Parameters
        ----------
        gid : int
            Global cell identifier
        morphology_file : str, optional
            Path to morphology file
        position : tuple, optional
            3D position (x, y, z) in microns
        """
        super().__init__(
            gid=gid,
            cell_type="PV_Basket",
            morphology_file=morphology_file,
            position=position,
        )

        self._define_parameters()

        if morphology_file:
            self._load_morphology()
        else:
            self._create_simplified_morphology()

        self.define_biophysics()
        self.insert_channels()
        self.setup_spike_detection()

    def _define_parameters(self):
        """Define biophysical parameters for PV+ basket cells."""
        self.biophys_params = {
            # Passive properties
            "Ra": 100.0,
            "cm": 1.0,
            "v_init": -70.0,

            # PV cells are fast-spiking due to high Na+ and K+ conductances
            "soma": {
                "gbar_nav16": 0.100,  # Much higher than pyramidal
                "gbar_kdr": 0.040,  # Much higher delayed rectifier
                "gbar_ka": 0.010,
                "g_leak": 0.0002,
                "e_leak": -70.0,
            },

            "dendrite": {
                "gbar_nav16": 0.030,
                "gbar_kdr": 0.015,
                "gbar_ka": 0.008,
                "g_leak": 0.0001,
                "e_leak": -70.0,
            },

            "axon": {
                "gbar_nav16": 0.500,  # Very high for fast spiking
                "gbar_kdr": 0.080,
                "g_leak": 0.0002,
                "e_leak": -70.0,
            },
        }

    def _create_simplified_morphology(self):
        """Create simplified basket cell morphology."""
        # Soma (smaller than pyramidal)
        self.soma = h.Section(name="soma")
        self.soma.L = 15  # um
        self.soma.diam = 15  # um
        self.soma.nseg = 1

        # Dendrites (aspiny, less complex than pyramidal)
        self.dends = []
        for i in range(6):  # More dendrites, shorter
            dend = h.Section(name=f"dend_{i}")
            dend.L = 100  # um (shorter than pyramidal)
            dend.diam = 1.5  # um
            dend.nseg = 7
            dend.connect(self.soma(0.5))
            self.dends.append(dend)

        # Extensive axon for widespread inhibition
        self.axon = []
        ais = h.Section(name="ais")
        ais.L = 20  # um
        ais.diam = 1.0  # um
        ais.nseg = 3
        ais.connect(self.soma(0))
        self.axon.append(ais)

        # Multiple axon collaterals
        for i in range(3):
            ax_coll = h.Section(name=f"axon_{i}")
            ax_coll.L = 400  # um
            ax_coll.diam = 0.8  # um
            ax_coll.nseg = 20
            ax_coll.connect(ais(1))
            self.axon.append(ax_coll)

        self.all_sections = [self.soma] + self.dends + self.axon

    def _load_morphology(self):
        """Load morphology from file."""
        print(f"Loading PV basket morphology from {self.morphology_file}")
        self._create_simplified_morphology()

    def define_biophysics(self):
        """Set passive properties."""
        for sec in self.all_sections:
            sec.Ra = self.biophys_params["Ra"]
            sec.cm = self.biophys_params["cm"]
            sec.insert("pas")

    def insert_channels(self):
        """Insert channels for fast-spiking properties."""
        params = self.biophys_params

        # Soma - high conductances for fast spiking
        self._insert_section_channels(self.soma, params["soma"])

        # Dendrites
        for dend in self.dends:
            self._insert_section_channels(dend, params["dendrite"])

        # Axon
        for ax in self.axon:
            self._insert_section_channels(ax, params["axon"])

    def _insert_section_channels(self, section, channel_params: dict):
        """Insert channels into section."""
        if "gbar_nav16" in channel_params:
            section.insert("nav16")
            section.gbar_nav16 = channel_params["gbar_nav16"]

        if "gbar_kdr" in channel_params:
            section.insert("kdr")
            section.gbar_kdr = channel_params["gbar_kdr"]

        if "gbar_ka" in channel_params:
            section.insert("ka")
            section.gbar_ka = channel_params["gbar_ka"]

        if "g_leak" in channel_params:
            section.insert("leak")
            section.g_leak = channel_params["g_leak"]
            section.e_leak = channel_params["e_leak"]

    def modify_for_cancer(self, modifications: dict):
        """Apply cancer-related parameter modifications."""
        print(f"Applying cancer modifications to PV basket cell {self.gid}")
        for param, value in modifications.items():
            print(f"  {param}: {value}")
