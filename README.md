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

### 🐳 Option 1: Docker (Recommended - No Manual Setup!)

**The easiest way to get started.** Docker handles all dependencies automatically.

#### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac/Linux)

#### Quick Start (3 commands!)
```bash
# 1. Clone repository
git clone <repository-url>
cd neurov2

# 2. Build Docker image (first time only, ~10 min)
# Windows:
docker-run.bat build

# Linux/Mac:
chmod +x docker-run.sh
./docker-run.sh build

# 3. Run a test simulation
# Windows:
docker-run.bat simulate 500 1000

# Linux/Mac:
./docker-run.sh simulate 500 1000
```

**That's it!** Results are saved to `./results/` folder.

**See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for complete Docker documentation.**

---

### 💻 Option 2: Manual Installation

If you prefer to install manually (requires Python 3.8-3.11):

#### Prerequisites
- Python 3.8-3.11 (NOT 3.12+, NEURON doesn't support it yet)
- NEURON 8.0+ with Python interface
- GCC/Clang compiler for .mod files

#### Setup

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

**Note**: If you encounter issues with NEURON installation, use Docker instead!

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

### Using Docker

```bash
# Run a simulation (500 cells, 1 second)
docker-run.bat simulate      # Windows
./docker-run.sh simulate     # Linux/Mac

# Analyze results
docker-run.bat analyze results/baseline_500cells.h5    # Windows
./docker-run.sh analyze results/baseline_500cells.h5   # Linux/Mac

# Start Jupyter for interactive analysis
docker-run.bat jupyter       # Windows
./docker-run.sh jupyter      # Linux/Mac
# Open http://localhost:8888
```

### Using Python Directly (after manual installation)

```python
from network.build_network import build_l23_network
from simulations.run_simulation import run_baseline_simulation

# Build network with default parameters
network = build_l23_network(n_cells=500)

# Run baseline simulation
runner = run_baseline_simulation(
    network,
    duration=1000,  # 1 second
    background_rate=5.0,
    output_file="results/test.h5"
)

# Analyze results
from analysis.basic_analysis import load_results, plot_raster
results = load_results("results/test.h5")
plot_raster(results['spikes'])
```

**See [docs/QUICKSTART.md](docs/QUICKSTART.md) for detailed examples and [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for Docker usage.**

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
