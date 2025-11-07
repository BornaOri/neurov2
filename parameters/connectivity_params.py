"""
Connectivity parameters for L2/3 barrel cortex based on experimental data.

Connection probabilities, synaptic weights, and delays from:
- Lefort et al. (2009) - L2/3 excitatory connections
- Holmgren et al. (2003) - Pyramidal-pyramidal connections
- Packer & Yuste (2011) - PV interneuron connectivity
- Silberberg & Markram (2007) - Interneuron connectivity
- Avermann et al. (2012) - Functional connectivity

Author: NeuroV2 Project
Date: 2025
"""

import numpy as np

# Connection probabilities P(pre -> post)
# Rows: presynaptic type, Columns: postsynaptic type
CONNECTION_PROBABILITIES = {
    # Pyramidal -> X
    ("L23_Pyramidal", "L23_Pyramidal"): 0.15,  # Lefort et al. 2009
    ("L23_Pyramidal", "PV_Basket"): 0.45,  # Strong recruitment
    ("L23_Pyramidal", "SST_Martinotti"): 0.35,
    ("L23_Pyramidal", "VIP_Interneuron"): 0.30,

    # PV Basket -> X (strong perisomatic inhibition)
    ("PV_Basket", "L23_Pyramidal"): 0.65,  # Packer & Yuste 2011
    ("PV_Basket", "PV_Basket"): 0.50,  # Mutual inhibition
    ("PV_Basket", "SST_Martinotti"): 0.45,
    ("PV_Basket", "VIP_Interneuron"): 0.40,

    # SST Martinotti -> X (dendritic inhibition)
    ("SST_Martinotti", "L23_Pyramidal"): 0.55,  # Silberberg & Markram 2007
    ("SST_Martinotti", "PV_Basket"): 0.30,
    ("SST_Martinotti", "SST_Martinotti"): 0.35,
    ("SST_Martinotti", "VIP_Interneuron"): 0.25,

    # VIP -> X (disinhibition - targets other interneurons)
    ("VIP_Interneuron", "L23_Pyramidal"): 0.10,  # Weak direct
    ("VIP_Interneuron", "PV_Basket"): 0.50,  # Disinhibition
    ("VIP_Interneuron", "SST_Martinotti"): 0.60,  # Strong disinhibition
    ("VIP_Interneuron", "VIP_Interneuron"): 0.30,
}

# Number of synaptic contacts per connection
# (mean, std) - can be multiple synapses per pair
SYNAPSES_PER_CONNECTION = {
    # Pyramidal -> X
    ("L23_Pyramidal", "L23_Pyramidal"): (3.5, 1.8),  # Markram et al. 1997
    ("L23_Pyramidal", "PV_Basket"): (4.0, 2.0),
    ("L23_Pyramidal", "SST_Martinotti"): (3.2, 1.5),
    ("L23_Pyramidal", "VIP_Interneuron"): (3.0, 1.5),

    # PV Basket -> X
    ("PV_Basket", "L23_Pyramidal"): (5.0, 2.5),  # Multiple perisomatic
    ("PV_Basket", "PV_Basket"): (3.5, 2.0),
    ("PV_Basket", "SST_Martinotti"): (3.0, 1.8),
    ("PV_Basket", "VIP_Interneuron"): (3.0, 1.8),

    # SST Martinotti -> X
    ("SST_Martinotti", "L23_Pyramidal"): (4.5, 2.2),  # Dendritic
    ("SST_Martinotti", "PV_Basket"): (3.0, 1.5),
    ("SST_Martinotti", "SST_Martinotti"): (2.5, 1.5),
    ("SST_Martinotti", "VIP_Interneuron"): (2.5, 1.5),

    # VIP -> X
    ("VIP_Interneuron", "L23_Pyramidal"): (2.0, 1.0),
    ("VIP_Interneuron", "PV_Basket"): (3.5, 1.8),
    ("VIP_Interneuron", "SST_Martinotti"): (4.0, 2.0),
    ("VIP_Interneuron", "VIP_Interneuron"): (2.5, 1.5),
}

# Synaptic weights (peak conductance in uS)
# (mean, std, min, max)
SYNAPTIC_WEIGHTS = {
    # Excitatory synapses (AMPA)
    ("L23_Pyramidal", "L23_Pyramidal", "AMPA"): (0.0005, 0.0002, 0.0001, 0.002),
    ("L23_Pyramidal", "PV_Basket", "AMPA"): (0.0008, 0.0003, 0.0002, 0.003),
    ("L23_Pyramidal", "SST_Martinotti", "AMPA"): (0.0006, 0.0002, 0.0001, 0.002),
    ("L23_Pyramidal", "VIP_Interneuron", "AMPA"): (0.0006, 0.0002, 0.0001, 0.002),

    # Excitatory synapses (NMDA) - ratio to AMPA ~0.4
    ("L23_Pyramidal", "L23_Pyramidal", "NMDA"): (0.0002, 0.0001, 0.00005, 0.001),
    ("L23_Pyramidal", "PV_Basket", "NMDA"): (0.0003, 0.00012, 0.0001, 0.0012),
    ("L23_Pyramidal", "SST_Martinotti", "NMDA"): (0.00024, 0.0001, 0.00005, 0.001),
    ("L23_Pyramidal", "VIP_Interneuron", "NMDA"): (0.00024, 0.0001, 0.00005, 0.001),

    # Inhibitory synapses (GABAA) - PV basket (strong)
    ("PV_Basket", "L23_Pyramidal", "GABAA"): (0.0012, 0.0004, 0.0003, 0.004),
    ("PV_Basket", "PV_Basket", "GABAA"): (0.0010, 0.0003, 0.0002, 0.003),
    ("PV_Basket", "SST_Martinotti", "GABAA"): (0.0010, 0.0003, 0.0002, 0.003),
    ("PV_Basket", "VIP_Interneuron", "GABAA"): (0.0010, 0.0003, 0.0002, 0.003),

    # Inhibitory synapses (GABAA) - SST Martinotti (moderate)
    ("SST_Martinotti", "L23_Pyramidal", "GABAA"): (0.0008, 0.0003, 0.0002, 0.003),
    ("SST_Martinotti", "PV_Basket", "GABAA"): (0.0007, 0.0002, 0.0002, 0.002),
    ("SST_Martinotti", "SST_Martinotti", "GABAA"): (0.0006, 0.0002, 0.0001, 0.002),
    ("SST_Martinotti", "VIP_Interneuron", "GABAA"): (0.0006, 0.0002, 0.0001, 0.002),

    # Inhibitory synapses (GABAB) - slow component (10% of GABAA)
    ("SST_Martinotti", "L23_Pyramidal", "GABAB"): (0.00008, 0.00003, 0.00002, 0.0003),

    # Inhibitory synapses (GABAA) - VIP interneuron
    ("VIP_Interneuron", "L23_Pyramidal", "GABAA"): (0.0005, 0.0002, 0.0001, 0.002),
    ("VIP_Interneuron", "PV_Basket", "GABAA"): (0.0008, 0.0003, 0.0002, 0.003),
    ("VIP_Interneuron", "SST_Martinotti", "GABAA"): (0.0009, 0.0003, 0.0002, 0.003),
    ("VIP_Interneuron", "VIP_Interneuron", "GABAA"): (0.0006, 0.0002, 0.0001, 0.002),
}

# Synaptic delays (ms) - (mean, std, min, max)
# Delays based on axonal conduction velocity and distance
SYNAPTIC_DELAYS = {
    # Short-range connections (local)
    ("L23_Pyramidal", "L23_Pyramidal"): (1.5, 0.5, 0.8, 4.0),
    ("L23_Pyramidal", "PV_Basket"): (1.2, 0.4, 0.8, 3.0),
    ("L23_Pyramidal", "SST_Martinotti"): (1.3, 0.4, 0.8, 3.0),
    ("L23_Pyramidal", "VIP_Interneuron"): (1.3, 0.4, 0.8, 3.0),

    # Fast-spiking interneurons (fast axonal conduction)
    ("PV_Basket", "L23_Pyramidal"): (0.8, 0.3, 0.5, 2.0),
    ("PV_Basket", "PV_Basket"): (0.8, 0.3, 0.5, 2.0),
    ("PV_Basket", "SST_Martinotti"): (0.8, 0.3, 0.5, 2.0),
    ("PV_Basket", "VIP_Interneuron"): (0.8, 0.3, 0.5, 2.0),

    # Martinotti (ascending axon - longer delays)
    ("SST_Martinotti", "L23_Pyramidal"): (2.0, 0.6, 1.0, 5.0),
    ("SST_Martinotti", "PV_Basket"): (1.5, 0.5, 0.8, 4.0),
    ("SST_Martinotti", "SST_Martinotti"): (1.5, 0.5, 0.8, 4.0),
    ("SST_Martinotti", "VIP_Interneuron"): (1.5, 0.5, 0.8, 4.0),

    # VIP interneurons
    ("VIP_Interneuron", "L23_Pyramidal"): (1.3, 0.4, 0.8, 3.5),
    ("VIP_Interneuron", "PV_Basket"): (1.2, 0.4, 0.8, 3.0),
    ("VIP_Interneuron", "SST_Martinotti"): (1.2, 0.4, 0.8, 3.0),
    ("VIP_Interneuron", "VIP_Interneuron"): (1.2, 0.4, 0.8, 3.0),
}

# Distance-dependent connection probability
# P(connection) decays with distance
CONNECTION_DISTANCE_PARAMS = {
    # (lambda - space constant in um, P0 - local probability)
    "L23_Pyramidal": {"lambda": 150.0, "P0": 0.20},  # Broader
    "PV_Basket": {"lambda": 200.0, "P0": 0.70},  # Wide inhibition
    "SST_Martinotti": {"lambda": 250.0, "P0": 0.60},  # Widespread
    "VIP_Interneuron": {"lambda": 120.0, "P0": 0.40},  # More local
}

# Synapse location preferences
# For pyramidal cells: where on the dendrite tree to place synapses
SYNAPSE_LOCATIONS = {
    # (section_type, distance_range_from_soma)
    ("L23_Pyramidal", "AMPA"): ("basal_apical", (20, 400)),  # Dendrites
    ("L23_Pyramidal", "NMDA"): ("basal_apical", (20, 400)),  # Co-localized
    ("PV_Basket", "GABAA"): ("soma", (0, 50)),  # Perisomatic
    ("SST_Martinotti", "GABAA"): ("apical", (100, 500)),  # Distal dendrites
    ("SST_Martinotti", "GABAB"): ("apical", (100, 500)),  # Co-localized
    ("VIP_Interneuron", "GABAA"): ("basal", (20, 200)),  # Proximal-mid
}


def get_connection_probability(pre_type: str, post_type: str) -> float:
    """Get connection probability between two cell types."""
    key = (pre_type, post_type)
    return CONNECTION_PROBABILITIES.get(key, 0.0)


def get_synaptic_parameters(pre_type: str, post_type: str, syn_type: str):
    """Get synaptic weight parameters."""
    key = (pre_type, post_type, syn_type)
    return SYNAPTIC_WEIGHTS.get(key, (0.0, 0.0, 0.0, 0.0))


def distance_dependent_probability(distance: float, pre_type: str) -> float:
    """
    Calculate distance-dependent connection probability.

    P(d) = P0 * exp(-d / lambda)

    Parameters
    ----------
    distance : float
        Distance between cells (um)
    pre_type : str
        Presynaptic cell type

    Returns
    -------
    prob : float
        Connection probability
    """
    params = CONNECTION_DISTANCE_PARAMS.get(pre_type, {"lambda": 100, "P0": 0.1})
    lambda_space = params["lambda"]
    P0 = params["P0"]

    return P0 * np.exp(-distance / lambda_space)
