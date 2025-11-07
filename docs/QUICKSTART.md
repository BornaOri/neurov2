# Quick Start Guide

Get started with the L2/3 barrel cortex simulation in minutes!

## Installation

### 1. Prerequisites

Ensure you have:
- Python 3.8+
- NEURON 8.0+ with Python interface
- GCC/Clang compiler

### 2. Clone and Install

```bash
git clone <repository-url>
cd neurov2

# Install Python dependencies
pip install -r requirements.txt

# Compile NEURON mechanisms
cd mechanisms
nrnivmodl
cd ..

# Install package
pip install -e .
```

## Running Your First Simulation

### Basic Example

```python
from network.build_network import build_l23_network
from simulations.run_simulation import run_baseline_simulation

# Build a small network (500 cells for quick testing)
network = build_l23_network(n_cells=500, seed=12345)

# Run baseline simulation (1 second)
runner = run_baseline_simulation(
    network,
    duration=1000,  # ms
    background_rate=5.0,  # Hz background input
    output_file="results/baseline_500cells.h5"
)
```

### Command-Line Usage

```bash
# Run simulation from command line
python -m simulations.run_simulation \
    --n-cells 500 \
    --duration 1000 \
    --background-rate 5.0 \
    --output results/baseline.h5
```

## Analyzing Results

### Basic Analysis

```python
from analysis.basic_analysis import (
    load_results,
    plot_raster,
    plot_firing_rates,
    plot_population_rate,
    print_summary_statistics
)

# Load results
results = load_results("results/baseline.h5")

# Print statistics
print_summary_statistics(results)

# Create plots
plot_raster(results['spikes'])
plot_firing_rates(results['spikes'], results['duration'])
plot_population_rate(results['spikes'], results['duration'])
```

### Command-Line Analysis

```bash
python -m analysis.basic_analysis results/baseline.h5
```

## Example Workflows

### 1. Spontaneous Activity

```python
network = build_l23_network(n_cells=1000)

runner = run_baseline_simulation(
    network,
    duration=2000,
    background_rate=3.0,
    output_file="results/spontaneous.h5"
)
```

### 2. Sensory Stimulation

```python
from simulations.run_simulation import SimulationRunner

network = build_l23_network(n_cells=1000)
runner = SimulationRunner(network)

# Add background activity
runner.add_background_input(rate=3.0)

# Stimulate a subset of pyramidal cells (simulating sensory input)
pyramidal_indices = [i for i, cell in enumerate(network.cells)
                     if cell.cell_type == "L23_Pyramidal"][:50]

runner.stimulate_cells(
    cell_indices=pyramidal_indices,
    start=500,
    duration=500,
    rate=40.0,  # Strong input
    weight=0.002
)

# Run simulation
runner.run(duration=2000)
runner.save_results("results/sensory_stim.h5")
```

### 3. Current Injection

```python
network = build_l23_network(n_cells=200)
runner = SimulationRunner(network)

# Inject current into first pyramidal cell
runner.inject_current(
    cell_index=0,
    amplitude=0.5,  # nA
    start=100,
    duration=800
)

runner.run(duration=1000)
runner.save_results("results/current_injection.h5")
```

## Modifying for Cancer Studies

### Example: Increase Sodium Channel Conductance

```python
from cells import L23Pyramidal

# Create cells with modified parameters for cancer
network = build_l23_network(n_cells=500)

# Modify all pyramidal cells
for cell in network.cells:
    if isinstance(cell, L23Pyramidal):
        # Increase Nav1.6 conductance by 20%
        for sec in [cell.soma] + cell.dends + cell.apic:
            sec.gbar_nav16 *= 1.2

        # Decrease K+ conductance by 10%
        for sec in [cell.soma] + cell.dends + cell.apic:
            sec.gbar_kdr *= 0.9

# Run simulation
runner = run_baseline_simulation(
    network,
    duration=1000,
    background_rate=5.0,
    output_file="results/cancer_modified.h5"
)
```

## Network Customization

### Custom Network Size and Density

```python
# Large network (computationally intensive)
large_network = build_l23_network(
    n_cells=5000,
    volume=(600, 600, 400),  # Larger volume
    seed=42
)

# Small test network
small_network = build_l23_network(
    n_cells=100,
    volume=(200, 200, 200),
    seed=1
)
```

### Custom Cell Type Proportions

```python
from cells import CELL_TYPE_PROPORTIONS

# Modify proportions (e.g., reduce inhibition)
CELL_TYPE_PROPORTIONS["L23_Pyramidal"] = 0.90  # Increase excitatory
CELL_TYPE_PROPORTIONS["PV_Basket"] = 0.05  # Decrease PV
CELL_TYPE_PROPORTIONS["SST_Martinotti"] = 0.03
CELL_TYPE_PROPORTIONS["VIP_Interneuron"] = 0.02

network = build_l23_network(n_cells=1000)
```

## Performance Tips

### For Large Networks (>2000 cells)

1. **Use parallel processing** (if available):
```python
from neuron import h
h.load_file("parcom.hoc")  # MPI support
```

2. **Reduce recording**:
```python
# Only record from subset of cells
for i, cell in enumerate(network.cells):
    if i % 10 != 0:  # Record every 10th cell
        cell.spike_times = None
```

3. **Increase time step** (with caution):
```python
runner = SimulationRunner(network, dt=0.05)  # Default is 0.025
```

## Troubleshooting

### NEURON mechanisms not found

```bash
cd mechanisms
nrnivmodl
# This should create x86_64/ (or similar) directory
```

### Memory issues with large networks

- Reduce network size
- Use simplified morphologies
- Disable unnecessary recordings

### Simulations run slowly

- Check dt (larger = faster but less accurate)
- Reduce network size for testing
- Use more efficient ion channel mechanisms

## Next Steps

- Review `/docs/ARCHITECTURE.md` for code organization
- Check `/mechanisms/README.md` for channel details
- See examples in `/docs/EXAMPLES.md`
- Read papers listed in main `README.md` for biological context

## Support

For issues or questions:
- Check the documentation in `/docs/`
- Review NEURON documentation: https://neuron.yale.edu/
- Open an issue on GitHub
