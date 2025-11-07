"""
Somatostatin-positive Martinotti Cell

Low-threshold spiking GABAergic interneuron.
Targets distal dendrites of pyramidal cells.
Based on Ma et al. (2006) and Markram et al. (2004).

Author: NeuroV2 Project
Date: 2025
"""

from neuron import h
from .base_cell import BaseCell


class SSTMartinotti(BaseCell):
    """Somatostatin-positive Martinotti cell (LTS interneuron)."""

    def __init__(
        self,
        gid: int,
        morphology_file: str = None,
        position: tuple = None,
    ):
        """
        Initialize SST+ Martinotti cell.

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
            cell_type="SST_Martinotti",
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
        """Define biophysical parameters for SST+ Martinotti cells."""
        self.biophys_params = {
            # Passive properties
            "Ra": 100.0,
            "cm": 1.0,
            "v_init": -70.0,

            # SST cells show low-threshold spiking due to T-type Ca channels
            "soma": {
                "gbar_nav16": 0.050,
                "gbar_kdr": 0.015,
                "gbar_ka": 0.008,
                "gbar_cat": 0.0003,  # High T-type Ca for LTS
                "gbar_sk": 0.0002,  # Ca-activated K
                "gbar_cal": 0.0001,
                "gbar_ih": 0.00005,
                "g_leak": 0.00015,
                "e_leak": -70.0,
            },

            "dendrite": {
                "gbar_nav16": 0.020,
                "gbar_kdr": 0.008,
                "gbar_ka": 0.010,
                "gbar_cat": 0.0002,
                "gbar_sk": 0.0001,
                "gbar_cal": 0.00008,
                "gbar_ih": 0.00008,
                "g_leak": 0.0001,
                "e_leak": -70.0,
            },

            "axon": {
                "gbar_nav16": 0.300,
                "gbar_kdr": 0.040,
                "gbar_ka": 0.015,
                "g_leak": 0.0002,
                "e_leak": -70.0,
            },

            # Calcium dynamics
            "ca_dynamics": {
                "depth": 0.1,
                "tau": 80.0,
                "cainf": 0.0001,
            },
        }

    def _create_simplified_morphology(self):
        """Create simplified Martinotti cell morphology."""
        # Soma
        self.soma = h.Section(name="soma")
        self.soma.L = 12  # um (small soma)
        self.soma.diam = 12  # um
        self.soma.nseg = 1

        # Dendrites (bitufted morphology characteristic)
        self.dends = []
        for i in range(4):
            dend = h.Section(name=f"dend_{i}")
            dend.L = 150  # um
            dend.diam = 1.2  # um
            dend.nseg = 9
            dend.connect(self.soma(0.5))
            self.dends.append(dend)

        # Ascending axon to layer 1 (characteristic of Martinotti)
        self.axon = []
        ais = h.Section(name="ais")
        ais.L = 15  # um
        ais.diam = 1.0  # um
        ais.nseg = 2
        ais.connect(self.soma(0))
        self.axon.append(ais)

        # Ascending axon to superficial layers
        ax_ascending = h.Section(name="axon_ascending")
        ax_ascending.L = 400  # um (reaches layer 1)
        ax_ascending.diam = 0.6  # um
        ax_ascending.nseg = 20
        ax_ascending.connect(ais(1))
        self.axon.append(ax_ascending)

        # Horizontal collaterals in layer 1
        for i in range(2):
            ax_coll = h.Section(name=f"axon_coll_{i}")
            ax_coll.L = 300  # um
            ax_coll.diam = 0.5  # um
            ax_coll.nseg = 15
            ax_coll.connect(ax_ascending(1))
            self.axon.append(ax_coll)

        self.all_sections = [self.soma] + self.dends + self.axon

    def _load_morphology(self):
        """Load morphology from file."""
        print(f"Loading SST Martinotti morphology from {self.morphology_file}")
        self._create_simplified_morphology()

    def define_biophysics(self):
        """Set passive properties."""
        for sec in self.all_sections:
            sec.Ra = self.biophys_params["Ra"]
            sec.cm = self.biophys_params["cm"]
            sec.insert("pas")

    def insert_channels(self):
        """Insert channels for low-threshold spiking."""
        params = self.biophys_params

        # Soma - with T-type Ca for LTS
        self._insert_section_channels(self.soma, params["soma"])
        self.soma.insert("cadyn")
        self.soma.depth_cadyn = params["ca_dynamics"]["depth"]
        self.soma.tau_cadyn = params["ca_dynamics"]["tau"]
        self.soma.cainf_cadyn = params["ca_dynamics"]["cainf"]

        # Dendrites
        for dend in self.dends:
            self._insert_section_channels(dend, params["dendrite"])
            dend.insert("cadyn")
            dend.depth_cadyn = params["ca_dynamics"]["depth"]
            dend.tau_cadyn = params["ca_dynamics"]["tau"]
            dend.cainf_cadyn = params["ca_dynamics"]["cainf"]

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

        if "gbar_cat" in channel_params:
            section.insert("cat")
            section.gbar_cat = channel_params["gbar_cat"]

        if "gbar_cal" in channel_params:
            section.insert("cal")
            section.gbar_cal = channel_params["gbar_cal"]

        if "gbar_sk" in channel_params:
            section.insert("sk")
            section.gbar_sk = channel_params["gbar_sk"]

        if "gbar_ih" in channel_params:
            section.insert("ih")
            section.gbar_ih = channel_params["gbar_ih"]

        if "g_leak" in channel_params:
            section.insert("leak")
            section.g_leak = channel_params["g_leak"]
            section.e_leak = channel_params["e_leak"]

    def modify_for_cancer(self, modifications: dict):
        """Apply cancer-related parameter modifications."""
        print(f"Applying cancer modifications to SST Martinotti cell {self.gid}")
        for param, value in modifications.items():
            print(f"  {param}: {value}")
