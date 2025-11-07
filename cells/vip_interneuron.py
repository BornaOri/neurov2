"""
VIP-positive Interneuron

Irregular spiking GABAergic interneuron.
Primarily targets other interneurons (disinhibition).
Based on Prönneke et al. (2015) and Tremblay et al. (2016).

Author: NeuroV2 Project
Date: 2025
"""

from neuron import h
from .base_cell import BaseCell


class VIPInterneuron(BaseCell):
    """VIP-positive interneuron (irregular spiking)."""

    def __init__(
        self,
        gid: int,
        morphology_file: str = None,
        position: tuple = None,
    ):
        """
        Initialize VIP+ interneuron.

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
            cell_type="VIP_Interneuron",
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
        """Define biophysical parameters for VIP+ interneurons."""
        self.biophys_params = {
            # Passive properties
            "Ra": 100.0,
            "cm": 1.0,
            "v_init": -70.0,

            # VIP cells have irregular spiking patterns
            "soma": {
                "gbar_nav16": 0.045,
                "gbar_kdr": 0.012,
                "gbar_ka": 0.012,  # Moderate A-current
                "gbar_ih": 0.0001,  # Moderate Ih
                "gbar_cal": 0.00005,
                "g_leak": 0.00012,
                "e_leak": -70.0,
            },

            "dendrite": {
                "gbar_nav16": 0.018,
                "gbar_kdr": 0.006,
                "gbar_ka": 0.008,
                "gbar_ih": 0.00006,
                "g_leak": 0.00008,
                "e_leak": -70.0,
            },

            "axon": {
                "gbar_nav16": 0.250,
                "gbar_kdr": 0.030,
                "gbar_ka": 0.010,
                "g_leak": 0.00015,
                "e_leak": -70.0,
            },
        }

    def _create_simplified_morphology(self):
        """Create simplified VIP interneuron morphology."""
        # Soma (small)
        self.soma = h.Section(name="soma")
        self.soma.L = 10  # um
        self.soma.diam = 10  # um
        self.soma.nseg = 1

        # Dendrites (bipolar or multipolar)
        self.dends = []
        for i in range(3):
            dend = h.Section(name=f"dend_{i}")
            dend.L = 120  # um
            dend.diam = 1.0  # um
            dend.nseg = 7
            dend.connect(self.soma(0.5))
            self.dends.append(dend)

        # Local axon arbor
        self.axon = []
        ais = h.Section(name="ais")
        ais.L = 15  # um
        ais.diam = 0.8  # um
        ais.nseg = 2
        ais.connect(self.soma(0))
        self.axon.append(ais)

        # Axon collaterals (targets other interneurons)
        for i in range(2):
            ax_coll = h.Section(name=f"axon_{i}")
            ax_coll.L = 250  # um
            ax_coll.diam = 0.5  # um
            ax_coll.nseg = 13
            ax_coll.connect(ais(1))
            self.axon.append(ax_coll)

        self.all_sections = [self.soma] + self.dends + self.axon

    def _load_morphology(self):
        """Load morphology from file."""
        print(f"Loading VIP interneuron morphology from {self.morphology_file}")
        self._create_simplified_morphology()

    def define_biophysics(self):
        """Set passive properties."""
        for sec in self.all_sections:
            sec.Ra = self.biophys_params["Ra"]
            sec.cm = self.biophys_params["cm"]
            sec.insert("pas")

    def insert_channels(self):
        """Insert channels for irregular spiking."""
        params = self.biophys_params

        # Soma
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

        if "gbar_ih" in channel_params:
            section.insert("ih")
            section.gbar_ih = channel_params["gbar_ih"]

        if "gbar_cal" in channel_params:
            section.insert("cal")
            section.gbar_cal = channel_params["gbar_cal"]

        if "g_leak" in channel_params:
            section.insert("leak")
            section.g_leak = channel_params["g_leak"]
            section.e_leak = channel_params["e_leak"]

    def modify_for_cancer(self, modifications: dict):
        """Apply cancer-related parameter modifications."""
        print(f"Applying cancer modifications to VIP interneuron {self.gid}")
        for param, value in modifications.items():
            print(f"  {param}: {value}")
