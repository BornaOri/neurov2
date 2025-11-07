# Jupyter Notebooks

Interactive notebooks for running and analyzing L2/3 simulations.

## Getting Started

### Using Docker (Recommended)

```bash
# Start Jupyter server
# Windows:
docker-run.bat jupyter

# Linux/Mac:
./docker-run.sh jupyter
```

Then open browser to: **http://localhost:8888**

### Manual Installation

```bash
# Install Jupyter
pip install jupyter ipykernel ipywidgets

# Start server
jupyter notebook
```

## Available Notebooks

### `example_simulation.ipynb`

Complete example showing:
1. Building a L2/3 network
2. Running baseline simulation
3. Analyzing spike data
4. Comparing control vs. cancer phenotypes
5. Generating plots

**Start here if you're new to the project!**

## Creating Your Own Notebooks

1. Start Jupyter server (see above)
2. Click "New" → "Python 3"
3. Import modules:

```python
import sys
sys.path.append('/app')  # If using Docker

from network.build_network import build_l23_network
from simulations.run_simulation import run_baseline_simulation
from analysis.basic_analysis import *
```

## Tips

### Saving Results

Results are automatically saved to `/app/results/` (Docker) or `./results/` (local).
These directories are persistent and accessible from your host machine.

### Memory Management

For large networks (>1000 cells), consider:
- Restarting kernel between runs
- Clearing unused variables with `del network`
- Using smaller networks for development

### Plotting

```python
import matplotlib.pyplot as plt

# Make plots appear in notebook
%matplotlib inline

# For interactive plots (optional)
%matplotlib widget
```

### Reloading Modified Code

If you edit Python modules and want to reload them:

```python
# Add at top of notebook
%load_ext autoreload
%autoreload 2
```

## Example Analyses

### Basic Spike Analysis

```python
from analysis.basic_analysis import load_results, plot_raster

results = load_results('results/my_simulation.h5')
plot_raster(results['spikes'])
```

### Compare Multiple Conditions

```python
import numpy as np
import matplotlib.pyplot as plt

# Load results
control = load_results('results/control.h5')
cancer = load_results('results/cancer.h5')

# Calculate firing rates
def calc_rates(spikes, duration):
    return [len(times)/(duration/1000) for times in spikes.values()]

control_rates = calc_rates(control['spikes'], control['duration'])
cancer_rates = calc_rates(cancer['spikes'], cancer['duration'])

# Plot comparison
plt.figure(figsize=(10, 4))
plt.hist(control_rates, bins=20, alpha=0.6, label='Control')
plt.hist(cancer_rates, bins=20, alpha=0.6, label='Cancer')
plt.xlabel('Firing Rate (Hz)')
plt.ylabel('Count')
plt.legend()
plt.show()

print(f"Control: {np.mean(control_rates):.2f} Hz")
print(f"Cancer: {np.mean(cancer_rates):.2f} Hz")
```

### Custom Network Modifications

```python
from cells import L23Pyramidal

network = build_l23_network(n_cells=500)

# Modify specific cells
for i, cell in enumerate(network.cells):
    if isinstance(cell, L23Pyramidal) and i < 50:
        # Modify first 50 pyramidal cells only
        for sec in cell.all_sections:
            if hasattr(sec, 'gbar_nav16'):
                sec.gbar_nav16 *= 1.5

# Run simulation with modifications
runner = run_baseline_simulation(network, duration=1000)
```

## Troubleshooting

### Kernel Keeps Dying

- Network too large (reduce `n_cells`)
- Not enough RAM allocated to Docker
- Try restarting Docker Desktop

### Modules Not Found

```python
# Make sure to add project to path
import sys
sys.path.append('/app')  # Docker
# or
sys.path.append('..')    # Local
```

### Plots Not Showing

```python
# Add this at top of notebook
%matplotlib inline
import matplotlib.pyplot as plt
```

### NEURON Not Found (Local Install)

Make sure NEURON is installed:
```bash
pip install neuron
```

Or use Docker (recommended).

## Resources

- [docs/QUICKSTART.md](../docs/QUICKSTART.md) - Getting started guide
- [docs/CANCER_MODIFICATIONS.md](../docs/CANCER_MODIFICATIONS.md) - Cancer parameter guide
- [DOCKER_GUIDE.md](../DOCKER_GUIDE.md) - Docker usage
