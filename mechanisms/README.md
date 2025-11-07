# NEURON Mechanisms

This directory contains NEURON `.mod` files defining ion channels and synaptic mechanisms for the L2/3 barrel cortex simulation.

## Compilation

To compile all mechanisms:

```bash
cd mechanisms
nrnivmodl
```

This will create a directory (platform-dependent, e.g., `x86_64/`) containing compiled shared libraries.

## Ion Channels

### Sodium Channels
- **nav16.mod** - Nav1.6 voltage-gated sodium channel
  - Fast activation and inactivation
  - Critical for action potential generation

### Potassium Channels
- **kdr.mod** - Delayed rectifier K+ channel
  - Slow activation, non-inactivating
  - Action potential repolarization

- **ka.mod** - A-type transient K+ channel
  - Fast activation and inactivation
  - Regulates dendritic excitability and spike timing

- **sk.mod** - Small-conductance Ca2+-activated K+ channel
  - Calcium-dependent activation
  - Mediates afterhyperpolarization (AHP)

### HCN Channels
- **ih.mod** - Hyperpolarization-activated cation current
  - Slow activation
  - Critical for dendritic integration and resonance
  - Mixed Na+/K+ conductance

### Calcium Channels
- **cal.mod** - L-type high voltage-activated Ca2+ channel
  - Slow inactivation
  - Important for calcium spikes and plateau potentials

- **can.mod** - N-type high voltage-activated Ca2+ channel
  - Medium inactivation
  - Predominantly dendritic

- **cat.mod** - T-type low voltage-activated Ca2+ channel
  - Fast inactivation
  - Active at subthreshold potentials
  - Important for burst firing

### Calcium Dynamics
- **cadyn.mod** - Intracellular calcium accumulation and decay
  - Tracks submembrane [Ca2+]
  - Drives Ca2+-dependent conductances

### Passive
- **leak.mod** - Passive leak conductance
  - Non-specific leak current

## Synaptic Mechanisms

### Excitatory
- **ampa.mod** - AMPA glutamate receptor
  - Fast rise (0.2 ms) and decay (2 ms)
  - Reversal: 0 mV

- **nmda.mod** - NMDA glutamate receptor
  - Slow rise (2 ms) and decay (50 ms)
  - Voltage-dependent Mg2+ block
  - Reversal: 0 mV

### Inhibitory
- **gabaa.mod** - GABA-A receptor
  - Fast rise (0.5 ms) and decay (10 ms)
  - Reversal: -70 mV (Cl-)

- **gabab.mod** - GABA-B receptor
  - Slow rise (50 ms) and decay (200 ms)
  - K+ conductance
  - Reversal: -90 mV

## Usage in Python

```python
from neuron import h

# Load mechanisms (after compilation)
h.load_file('stdrun.hoc')

# Create a section
soma = h.Section(name='soma')

# Insert ion channels
soma.insert('nav16')
soma.insert('kdr')
soma.insert('ka')
soma.insert('sk')
soma.insert('cadyn')
soma.insert('leak')

# Set conductances
soma.gbar_nav16 = 0.040  # S/cm2
soma.gbar_kdr = 0.010
soma.gbar_ka = 0.015

# Add synapse
syn = h.AMPA(soma(0.5))
syn.gmax = 0.001  # uS
```

## Modifying for Cancer Studies

Key parameters that may change in cancer-affected tissue:

1. **Ion Channel Conductances** (`gbar`):
   - Altered expression levels
   - Example: `soma.gbar_nav16 *= 1.2` (20% increase)

2. **Activation/Inactivation** (voltage dependence):
   - Shifts in `vhalf` parameters
   - Changes in slope factors (`k`)

3. **Kinetics** (time constants):
   - Altered `tau` parameters
   - Slower/faster channel dynamics

4. **Synaptic Parameters**:
   - Changed `gmax` (receptor density)
   - Altered time constants (rise/decay)

## References

- Hu et al. (2009) - Nav channels in hippocampus
- Korngreen & Sakmann (2000) - K channels in cortical pyramids
- Destexhe et al. (1998) - Synaptic mechanisms
- Magee (1998) - Ih in dendrites
- Markram et al. (2015) - Blue Brain Project cortical channels
