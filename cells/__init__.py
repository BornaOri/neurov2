"""
Cell models for L2/3 barrel cortex simulation.

Includes excitatory and inhibitory neuron types with biorealistic properties.

Author: NeuroV2 Project
Date: 2025
"""

from .base_cell import BaseCell
from .l23_pyramidal import L23Pyramidal
from .pv_basket import PVBasket
from .sst_martinotti import SSTMartinotti
from .vip_interneuron import VIPInterneuron

__all__ = [
    "BaseCell",
    "L23Pyramidal",
    "PVBasket",
    "SSTMartinotti",
    "VIPInterneuron",
]

# Cell type proportions based on experimental data
# From Lefort et al. (2009), Meyer et al. (2010)
CELL_TYPE_PROPORTIONS = {
    "L23_Pyramidal": 0.82,  # 82% excitatory
    "PV_Basket": 0.072,  # 40% of 18% inhibitory = 7.2%
    "SST_Martinotti": 0.054,  # 30% of 18% inhibitory = 5.4%
    "VIP_Interneuron": 0.027,  # 15% of 18% inhibitory = 2.7%
    "Other_Inhibitory": 0.027,  # Remaining 15% = 2.7%
}

# Map cell type names to classes
CELL_TYPE_CLASSES = {
    "L23_Pyramidal": L23Pyramidal,
    "PV_Basket": PVBasket,
    "SST_Martinotti": SSTMartinotti,
    "VIP_Interneuron": VIPInterneuron,
}


def create_cell(gid: int, cell_type: str, **kwargs):
    """
    Factory function to create cells of specified type.

    Parameters
    ----------
    gid : int
        Global cell identifier
    cell_type : str
        Type of cell to create
    **kwargs : dict
        Additional parameters for cell constructor

    Returns
    -------
    cell : BaseCell
        Instantiated cell object
    """
    if cell_type not in CELL_TYPE_CLASSES:
        raise ValueError(
            f"Unknown cell type: {cell_type}. "
            f"Available types: {list(CELL_TYPE_CLASSES.keys())}"
        )

    cell_class = CELL_TYPE_CLASSES[cell_type]
    return cell_class(gid=gid, **kwargs)
