# L2/3 Barrel Cortex Biorealistic Simulation

A morphologically detailed, biophysically realistic simulation of rodent primary somatosensory cortex (S1) Layer 2/3 using NEURON.

## Project Overview

This simulation models a ~2,000-3,000 neuron microcircuit of barrel cortex L2/3 with:
- **Morphologically detailed neurons** with multi-compartment models
- **Complex ion channel dynamics** (Nav1.6, Kv, Kca, Ih, Ca channels)
- **Biorealistic cell type proportions** based on experimental data
- **Anatomically constrained connectivity** from published literature
- **Realistic network scale** matching cortical density

### Cell Types Included

**Excitatory (~80-85%)**:
- L2/3 Pyramidal cells (multiple subtypes)

**Inhibitory (~15-20%)**:
- Parvalbumin+ (PV) basket/chandelier cells (~40% of inhibitory)
- Somatostatin+ (SST) Martinotti cells (~30% of inhibitory)
- VIP+ interneurons (~15% of inhibitory)
- Other GABAergic interneurons (~15% of inhibitory)

## Research Goal

Investigate the effects of cancer on cortical circuit dynamics by modifying biophysical parameters based on experimental findings from cancer-affected cortical tissue.

## Installation

### Prerequisites
- Python 3.8+
- NEURON 8.0+ with Python interface
- GCC/Clang compiler for .mod files

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd neurov2

# Install Python dependencies
pip install -r requirements.txt

# Compile NEURON mechanisms
cd mechanisms
nrnivmodl
cd ..

# Install package in development mode
pip install -e .
```

## Project Structure

```
neurov2/
├── cells/              # Neuron model definitions
├── mechanisms/         # NEURON .mod files (ion channels, synapses)
├── morphologies/       # SWC morphology files
├── network/           # Network building and connectivity
├── simulations/       # Simulation runners and protocols
├── parameters/        # Cell and network parameters
├── analysis/          # Analysis and visualization tools
├── data/              # Input data and experimental datasets
├── results/           # Simulation outputs
└── docs/              # Documentation
```

## Quick Start

```python
from network.build_network import build_l23_network
from simulations.run_simulation import run_baseline_simulation

# Build network with default parameters
network = build_l23_network(n_neurons=2000)

# Run baseline simulation
results = run_baseline_simulation(network, duration=1000)  # 1 second

# Analyze results
from analysis.visualization import plot_raster, plot_lfp
plot_raster(results)
plot_lfp(results)
```

## Key References

### L2/3 Barrel Cortex Anatomy & Connectivity
- Lefort et al. (2009) "The excitatory neuronal network of L2-3 barrel cortex" Neuron
- Avermann et al. (2012) "Microcircuits of excitatory and inhibitory neurons" J Neurosci
- Packer & Yuste (2011) "Dense, unspecific connectivity of neocortical PV interneurons" J Neurosci
- Feldmeyer et al. (2002) "Synaptic connections between L2/3 pyramidal neurons" J Physiol

### Biophysical Properties
- Markram et al. (2015) "Reconstruction and simulation of neocortical microcircuitry" Cell
- Hay et al. (2011) "Models of neocortical L5b pyramidal cells" PLoS Comp Bio
- Almog & Korngreen (2014) "A quantitative description of dendritic conductances" J Neurosci

### Ion Channel Models
- Hu et al. (2009) "Dendritic mechanisms of phase precession" Hippocampus
- Migliore et al. (2018) "Role of functional diversity in cortical circuits" eLife

## License

MIT License

## Authors

Created for investigating cortical effects of cancer on neural dynamics.

## Citation

If you use this code, please cite:
```
[Citation to be added upon publication]
```
