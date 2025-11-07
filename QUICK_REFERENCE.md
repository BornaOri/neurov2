# NeuROV2 Quick Reference

## 🚀 Getting Started (Docker)

### First Time Setup
```bash
# 1. Install Docker Desktop from docker.com
# 2. Clone repository
git clone <repository-url>
cd neurov2

# 3. Build image (10 minutes, only once)
docker-run.bat build          # Windows
./docker-run.sh build         # Linux/Mac
```

### Test Installation
```bash
docker-run.bat test           # Windows
./docker-run.sh test          # Linux/Mac
```

---

## 📋 Common Commands

### Run Simulations
```bash
# Small test (500 cells, 1 second)
docker-run.bat simulate

# Custom size
docker-run.bat simulate [n_cells] [duration_ms]
docker-run.bat simulate 1000 2000    # 1000 cells, 2 seconds
```

### Analyze Results
```bash
docker-run.bat analyze results/baseline_500cells.h5
```

### Interactive Shell
```bash
docker-run.bat bash
# Now you're inside the container!
python
>>> from network.build_network import build_l23_network
>>> network = build_l23_network(n_cells=100)
```

### Jupyter Notebooks
```bash
docker-run.bat jupyter
# Open browser to http://localhost:8888
```

---

## 🧬 Cancer Modification Template

```python
from network.build_network import build_l23_network
from simulations.run_simulation import run_baseline_simulation
from cells import L23Pyramidal

# Build network
network = build_l23_network(n_cells=1000, seed=42)

# Apply cancer phenotype
for cell in network.cells:
    if isinstance(cell, L23Pyramidal):
        # Increase Nav channels (hyperexcitability)
        for sec in [cell.soma] + cell.dends + cell.apic:
            sec.gbar_nav16 *= 1.25  # 25% increase

        # Decrease K+ channels
        for sec in [cell.soma] + cell.dends + cell.apic:
            sec.gbar_kdr *= 0.80    # 20% decrease

# Run simulation
runner = run_baseline_simulation(
    network,
    duration=2000,
    background_rate=5.0,
    output_file="results/cancer.h5"
)
```

---

## 📊 Quick Analysis

```python
from analysis.basic_analysis import *

# Load results
results = load_results("results/baseline_500cells.h5")

# Print statistics
print_summary_statistics(results)

# Create plots
plot_raster(results['spikes'])
plot_firing_rates(results['spikes'], results['duration'])
plot_population_rate(results['spikes'], results['duration'])

# Calculate synchrony
sync = calculate_synchrony(results['spikes'], results['duration'])
print(f"Network synchrony: {sync:.3f}")
```

---

## 🗂️ Project Structure

```
neurov2/
├── cells/                    # Neuron models
│   ├── l23_pyramidal.py     # Excitatory neurons
│   ├── pv_basket.py         # Fast-spiking inhibition
│   ├── sst_martinotti.py    # Dendritic inhibition
│   └── vip_interneuron.py   # Disinhibition
│
├── mechanisms/               # Ion channels (.mod files)
│   ├── nav16.mod            # Sodium channel
│   ├── kdr.mod, ka.mod      # Potassium channels
│   ├── cal.mod, can.mod     # Calcium channels
│   └── ampa.mod, gabaa.mod  # Synapses
│
├── network/                  # Network building
│   └── build_network.py     # Main network constructor
│
├── parameters/               # Connectivity parameters
│   └── connectivity_params.py
│
├── simulations/              # Simulation runners
│   └── run_simulation.py
│
├── analysis/                 # Analysis tools
│   └── basic_analysis.py
│
├── results/                  # Output files (.h5)
│
└── notebooks/                # Jupyter notebooks
    └── example_simulation.ipynb
```

---

## 🔧 Modifying Parameters

### Cell Parameters
```python
cell.soma.gbar_nav16 *= 1.2   # Increase Nav by 20%
cell.soma.gbar_kdr *= 0.8     # Decrease Kdr by 20%
cell.soma.gbar_ih *= 1.5      # Increase Ih by 50%
```

### Synaptic Weights
```python
from parameters.connectivity_params import SYNAPTIC_WEIGHTS

# Modify before building network
key = ("L23_Pyramidal", "PV_Basket", "AMPA")
mean, std, min_val, max_val = SYNAPTIC_WEIGHTS[key]
SYNAPTIC_WEIGHTS[key] = (mean * 1.2, std, min_val, max_val * 1.2)
```

### Connection Probabilities
```python
from parameters.connectivity_params import CONNECTION_PROBABILITIES

# Modify before building network
CONNECTION_PROBABILITIES[("L23_Pyramidal", "L23_Pyramidal")] *= 1.15
```

---

## 📈 Performance Tips

### Network Size Guidelines
- **Testing**: 100-500 cells (~1-5 minutes)
- **Development**: 500-1000 cells (~5-20 minutes)
- **Production**: 2000-5000 cells (~30-120 minutes)

### Speed Up Simulations
1. Reduce network size for testing
2. Decrease simulation duration
3. Increase time step (with caution): `dt=0.05` instead of `0.025`
4. Allocate more CPU/RAM in `docker-compose.yml`

### Memory Management
```yaml
# Edit docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '8'      # Increase CPUs
      memory: 16G    # Increase RAM
```

---

## 🐛 Troubleshooting

### Docker Issues
```bash
# Docker not running
# → Start Docker Desktop

# Image build fails
docker-compose build --no-cache neurov2

# Port 8888 in use (Jupyter)
# → Edit docker-compose.yml, change "8888:8888" to "8889:8888"
```

### Simulation Issues
```bash
# Out of memory
# → Reduce n_cells or increase Docker RAM

# Slow simulation
# → Check CPU allocation in docker-compose.yml
# → Reduce network size for testing

# Results not found
mkdir -p results
```

---

## 📚 Documentation Files

- **README.md** - Project overview
- **DOCKER_GUIDE.md** - Complete Docker documentation (⭐ READ THIS)
- **docs/QUICKSTART.md** - Detailed examples
- **docs/CANCER_MODIFICATIONS.md** - Cancer parameter guide
- **mechanisms/README.md** - Ion channel details
- **notebooks/README.md** - Jupyter guide

---

## 🎯 Typical Workflow

```bash
# 1. Run control simulation
docker-run.bat simulate 1000 2000

# 2. Run cancer simulation (in shell)
docker-run.bat bash
# Inside container:
python
>>> # Apply cancer modifications and run
>>> # (see Cancer Modification Template above)

# 3. Compare results in Jupyter
docker-run.bat jupyter
# Open notebooks/example_simulation.ipynb
```

---

## 💡 Tips

- **Start small**: Test with 100-500 cells before scaling up
- **Use Jupyter**: Best for interactive analysis
- **Save results**: Everything in `./results/` is persistent
- **Git ignore**: Results (.h5) are already in .gitignore
- **Documentation**: Use `help()` function in Python
- **Check logs**: `docker-compose logs` for debugging

---

## 🆘 Getting Help

1. Check **DOCKER_GUIDE.md** for Docker issues
2. Check **docs/QUICKSTART.md** for usage examples
3. Check **docs/CANCER_MODIFICATIONS.md** for parameter guidance
4. Run `docker-run.bat help` for command list
5. Open an issue on GitHub

---

## ⚡ One-Line Examples

```bash
# Quick test
docker-run.bat test

# Small simulation
docker-run.bat simulate

# Large simulation
docker-run.bat simulate 5000 5000

# Analyze specific file
docker-run.bat analyze results/my_simulation.h5

# Interactive Python
docker-run.bat bash

# Jupyter notebook
docker-run.bat jupyter

# Rebuild from scratch
docker-run.bat build

# Clean up
docker-run.bat clean
```

---

**Need more details? See [DOCKER_GUIDE.md](DOCKER_GUIDE.md)**
