"""
Layer 2/3 Pyramidal Cell

Morphologically detailed pyramidal neuron with realistic channel distributions.
Based on Larkum et al. (2009), Hay et al. (2011), and Markram et al. (2015).

Author: NeuroV2 Project
Date: 2025
"""

from neuron import h
import numpy as np
from .base_cell import BaseCell


class L23Pyramidal(BaseCell):
    """Layer 2/3 pyramidal neuron."""

    def __init__(
        self,
        gid: int,
        morphology_file: str = None,
        position: tuple = None,
    ):
        """
        Initialize L2/3 pyramidal cell.

        Parameters
        ----------
        gid : int
            Global cell identifier
        morphology_file : str, optional
            Path to morphology file (SWC or ASC format)
        position : tuple, optional
            3D position (x, y, z) in microns
        """
        super().__init__(
            gid=gid,
            cell_type="L23_Pyramidal",
            morphology_file=morphology_file,
            position=position,
        )

        # Define biophysical parameters
        self._define_parameters()

        # Build cell
        if morphology_file:
            self._load_morphology()
        else:
            self._create_simplified_morphology()

        self.define_biophysics()
        self.insert_channels()
        self.setup_spike_detection()

    def _define_parameters(self):
        """Define biophysical parameters for L2/3 pyramidal cells."""
        self.biophys_params = {
            # Passive properties
            "Ra": 100.0,  # Axial resistance (Ohm*cm)
            "cm": 1.0,  # Membrane capacitance (uF/cm2)
            "v_init": -70.0,  # Initial voltage (mV)

            # Reversal potentials
            "ena": 50.0,  # Sodium
            "ek": -90.0,  # Potassium
            "eca": 140.0,  # Calcium

            # Soma conductances (S/cm2)
            "soma": {
                "gbar_nav16": 0.040,
                "gbar_kdr": 0.010,
                "gbar_ka": 0.002,
                "gbar_sk": 0.0001,
                "gbar_cal": 0.00005,
                "gbar_can": 0.00003,
                "gbar_cat": 0.00001,
                "gbar_ih": 0.00002,
                "g_leak": 0.0001,
                "e_leak": -70.0,
            },

            # Basal dendrite conductances (S/cm2)
            "basal": {
                "gbar_nav16": 0.020,
                "gbar_kdr": 0.008,
                "gbar_ka": 0.010,
                "gbar_sk": 0.00005,
                "gbar_cal": 0.0001,
                "gbar_can": 0.0002,
                "gbar_cat": 0.00005,
                "gbar_ih": 0.00005,
                "g_leak": 0.00005,
                "e_leak": -70.0,
            },

            # Apical dendrite conductances (S/cm2)
            "apical": {
                "gbar_nav16": 0.015,
                "gbar_kdr": 0.005,
                "gbar_ka": 0.015,  # Higher in apical dendrites
                "gbar_sk": 0.00005,
                "gbar_cal": 0.0002,  # Higher Ca channels
                "gbar_can": 0.0003,
                "gbar_cat": 0.0001,
                "gbar_ih": 0.0001,  # Increases with distance
                "g_leak": 0.00005,
                "e_leak": -70.0,
            },

            # Axon conductances (S/cm2)
            "axon": {
                "gbar_nav16": 0.400,  # Very high Na in axon
                "gbar_kdr": 0.040,
                "gbar_ka": 0.010,
                "g_leak": 0.0001,
                "e_leak": -70.0,
            },

            # Calcium dynamics
            "ca_dynamics": {
                "depth": 0.1,  # Shell depth (um)
                "tau": 80.0,  # Decay time (ms)
                "cainf": 0.0001,  # Resting [Ca] (mM)
            },
        }

    def _create_simplified_morphology(self):
        """Create simplified multi-compartment morphology."""
        # Soma
        self.soma = h.Section(name="soma")
        self.soma.L = 20  # um
        self.soma.diam = 20  # um
        self.soma.nseg = 1

        # Basal dendrites (4 branches)
        self.dends = []
        for i in range(4):
            dend = h.Section(name=f"basal_{i}")
            dend.L = 200  # um
            dend.diam = 2  # um (tapering could be added)
            dend.nseg = 11  # Odd number for middle segment
            dend.connect(self.soma(0.5))
            self.dends.append(dend)

        # Apical dendrites (trunk + tuft)
        apic_trunk = h.Section(name="apic_trunk")
        apic_trunk.L = 300  # um
        apic_trunk.diam = 2.5  # um
        apic_trunk.nseg = 15
        apic_trunk.connect(self.soma(1))
        self.apic.append(apic_trunk)

        # Apical tuft branches (3 branches)
        for i in range(3):
            apic_tuft = h.Section(name=f"apic_tuft_{i}")
            apic_tuft.L = 200  # um
            apic_tuft.diam = 1.5  # um
            apic_tuft.nseg = 11
            apic_tuft.connect(apic_trunk(1))
            self.apic.append(apic_tuft)

        # Axon
        ais = h.Section(name="ais")  # Initial segment
        ais.L = 30  # um
        ais.diam = 1.5  # um
        ais.nseg = 5
        ais.connect(self.soma(0))
        self.axon.append(ais)

        axon_proper = h.Section(name="axon")
        axon_proper.L = 500  # um
        axon_proper.diam = 1.0  # um
        axon_proper.nseg = 25
        axon_proper.connect(ais(1))
        self.axon.append(axon_proper)

        # Collect all sections
        self.all_sections = [self.soma] + self.dends + self.apic + self.axon

    def _load_morphology(self):
        """Load morphology from SWC file."""
        # TODO: Implement SWC loading using Import3d
        print(f"Loading morphology from {self.morphology_file}")
        # For now, fall back to simplified
        self._create_simplified_morphology()

    def define_biophysics(self):
        """Set passive properties for all sections."""
        for sec in self.all_sections:
            sec.Ra = self.biophys_params["Ra"]
            sec.cm = self.biophys_params["cm"]
            sec.insert("pas")

    def insert_channels(self):
        """Insert active channels with realistic distributions."""
        params = self.biophys_params

        # Soma
        self._insert_section_channels(self.soma, params["soma"])
        self.soma.insert("cadyn")
        self.soma.depth_cadyn = params["ca_dynamics"]["depth"]
        self.soma.tau_cadyn = params["ca_dynamics"]["tau"]
        self.soma.cainf_cadyn = params["ca_dynamics"]["cainf"]

        # Basal dendrites
        for dend in self.dends:
            self._insert_section_channels(dend, params["basal"])
            dend.insert("cadyn")
            dend.depth_cadyn = params["ca_dynamics"]["depth"]
            dend.tau_cadyn = params["ca_dynamics"]["tau"]
            dend.cainf_cadyn = params["ca_dynamics"]["cainf"]

        # Apical dendrites (with distance-dependent Ih)
        for i, apic in enumerate(self.apic):
            self._insert_section_channels(apic, params["apical"])
            apic.insert("cadyn")
            apic.depth_cadyn = params["ca_dynamics"]["depth"]
            apic.tau_cadyn = params["ca_dynamics"]["tau"]
            apic.cainf_cadyn = params["ca_dynamics"]["cainf"]

            # Increase Ih with distance from soma
            for seg in apic:
                distance = h.distance(seg.x, sec=apic)
                seg.gbar_ih = params["apical"]["gbar_ih"] * (1 + distance / 100)

        # Axon (high Na+ channels)
        for ax in self.axon:
            self._insert_section_channels(ax, params["axon"])

    def _insert_section_channels(self, section, channel_params: dict):
        """
        Insert ion channels into a section.

        Parameters
        ----------
        section : h.Section
            NEURON section
        channel_params : dict
            Dictionary of channel parameters
        """
        # Sodium
        if "gbar_nav16" in channel_params:
            section.insert("nav16")
            section.gbar_nav16 = channel_params["gbar_nav16"]

        # Potassium
        if "gbar_kdr" in channel_params:
            section.insert("kdr")
            section.gbar_kdr = channel_params["gbar_kdr"]

        if "gbar_ka" in channel_params:
            section.insert("ka")
            section.gbar_ka = channel_params["gbar_ka"]

        if "gbar_sk" in channel_params:
            section.insert("sk")
            section.gbar_sk = channel_params["gbar_sk"]

        # Calcium
        if "gbar_cal" in channel_params:
            section.insert("cal")
            section.gbar_cal = channel_params["gbar_cal"]

        if "gbar_can" in channel_params:
            section.insert("can")
            section.gbar_can = channel_params["gbar_can"]

        if "gbar_cat" in channel_params:
            section.insert("cat")
            section.gbar_cat = channel_params["gbar_cat"]

        # HCN
        if "gbar_ih" in channel_params:
            section.insert("ih")
            section.gbar_ih = channel_params["gbar_ih"]

        # Leak
        if "g_leak" in channel_params:
            section.insert("leak")
            section.g_leak = channel_params["g_leak"]
            section.e_leak = channel_params["e_leak"]

    def modify_for_cancer(self, modifications: dict):
        """
        Modify cell parameters to simulate cancer effects.

        Parameters
        ----------
        modifications : dict
            Dictionary of parameter modifications
            Example: {
                'soma_nav16_scale': 1.2,  # 20% increase
                'dendrite_ka_scale': 0.8,  # 20% decrease
            }
        """
        # This is a placeholder for future cancer parameter modifications
        # Will be filled in based on literature review
        print(f"Applying cancer modifications to cell {self.gid}")
        for param, value in modifications.items():
            print(f"  {param}: {value}")
