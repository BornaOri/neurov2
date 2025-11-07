# Cancer-Related Modifications Guide

This document outlines how to modify the L2/3 barrel cortex simulation to study cancer effects on neural dynamics.

## Overview

Cancer and cancer treatments can affect neural circuits through multiple mechanisms:
1. **Altered ion channel expression** (chemotherapy-induced changes)
2. **Disrupted excitatory/inhibitory balance**
3. **Modified synaptic transmission**
4. **Metabolic alterations**
5. **Inflammatory effects on excitability**

## Parameter Modification Strategy

### 1. Ion Channel Modifications

#### Sodium Channels (Hyperexcitability)

Studies show increased Nav channel expression in peritumoral tissue:

```python
# Increase Nav1.6 conductance
for cell in network.cells:
    if isinstance(cell, L23Pyramidal):
        for sec in [cell.soma] + cell.dends + cell.apic:
            sec.gbar_nav16 *= 1.3  # 30% increase
```

**Evidence**:
- Campbell et al. (2015) - Nav1.6 upregulation in tumor microenvironment
- Venkataramani et al. (2019) - Neuronal activity in glioma

#### Potassium Channels (Impaired Repolarization)

Decreased K+ currents lead to prolonged action potentials:

```python
# Decrease delayed rectifier K+ channels
for cell in network.cells:
    for sec in cell.all_sections:
        if hasattr(sec, 'gbar_kdr'):
            sec.gbar_kdr *= 0.7  # 30% decrease
```

#### Calcium Channels (Altered Ca2+ Dynamics)

```python
# Increase L-type Ca channels
for cell in network.cells:
    if isinstance(cell, L23Pyramidal):
        for sec in cell.apic:  # Particularly in dendrites
            sec.gbar_cal *= 1.4
```

### 2. Synaptic Modifications

#### Enhanced Excitatory Transmission

```python
# Increase AMPA receptor conductance
from parameters.connectivity_params import SYNAPTIC_WEIGHTS

for key in SYNAPTIC_WEIGHTS:
    if "AMPA" in key:
        mean, std, min_val, max_val = SYNAPTIC_WEIGHTS[key]
        SYNAPTIC_WEIGHTS[key] = (mean * 1.2, std, min_val, max_val * 1.2)
```

#### Reduced Inhibition

```python
# Decrease GABAergic transmission
for key in SYNAPTIC_WEIGHTS:
    if "GABA" in key:
        mean, std, min_val, max_val = SYNAPTIC_WEIGHTS[key]
        SYNAPTIC_WEIGHTS[key] = (mean * 0.8, std, min_val * 0.8, max_val)
```

### 3. Network-Level Changes

#### Altered Connectivity (Structural Plasticity)

```python
# Increase excitatory connection probability
from parameters.connectivity_params import CONNECTION_PROBABILITIES

for key in CONNECTION_PROBABILITIES:
    pre_type, post_type = key
    if "Pyramidal" in pre_type:
        CONNECTION_PROBABILITIES[key] *= 1.15  # 15% increase
```

#### Reduced Inhibitory Neuron Function

```python
# Selectively modify PV interneurons
for cell in network.cells:
    if isinstance(cell, PVBasket):
        # Reduce excitability
        cell.soma.gbar_nav16 *= 0.85

        # Reduce output (via synapse modification)
        for syn in cell.synapses['GABAA']:
            syn.gmax *= 0.8
```

## Example: Complete Cancer Phenotype

```python
def apply_cancer_phenotype(network, severity='moderate'):
    """
    Apply cancer-related modifications to network.

    Parameters
    ----------
    network : L23Network
        Network to modify
    severity : str
        'mild', 'moderate', or 'severe'
    """

    # Define severity-dependent scaling factors
    severity_scales = {
        'mild': {
            'nav_increase': 1.1,
            'kdr_decrease': 0.95,
            'gaba_decrease': 0.95,
        },
        'moderate': {
            'nav_increase': 1.25,
            'kdr_decrease': 0.80,
            'gaba_decrease': 0.85,
        },
        'severe': {
            'nav_increase': 1.5,
            'kdr_decrease': 0.65,
            'gaba_decrease': 0.70,
        }
    }

    scales = severity_scales[severity]

    print(f"Applying {severity} cancer phenotype...")

    # 1. Modify ion channels
    for cell in network.cells:
        # Increase Nav channels (hyperexcitability)
        for sec in cell.all_sections:
            if hasattr(sec, 'gbar_nav16'):
                sec.gbar_nav16 *= scales['nav_increase']

        # Decrease K+ channels
        for sec in cell.all_sections:
            if hasattr(sec, 'gbar_kdr'):
                sec.gbar_kdr *= scales['kdr_decrease']

    # 2. Modify inhibitory synapses
    for cell in network.cells:
        for syn_type in ['GABAA', 'GABAB']:
            for syn in cell.synapses[syn_type]:
                syn.gmax *= scales['gaba_decrease']

    print("Cancer phenotype applied successfully")


# Usage
network = build_l23_network(n_cells=1000)

# Apply modifications
apply_cancer_phenotype(network, severity='moderate')

# Run simulation
runner = run_baseline_simulation(
    network,
    duration=2000,
    background_rate=5.0,
    output_file="results/cancer_moderate.h5"
)
```

## Comparing Control vs. Cancer

```python
def compare_control_vs_cancer():
    """Compare network activity in control and cancer conditions."""

    # Control network
    print("Running control simulation...")
    control_net = build_l23_network(n_cells=1000, seed=12345)
    control_runner = run_baseline_simulation(
        control_net,
        duration=2000,
        background_rate=5.0,
        output_file="results/control.h5"
    )

    # Cancer network (same seed for matched comparison)
    print("\nRunning cancer simulation...")
    cancer_net = build_l23_network(n_cells=1000, seed=12345)
    apply_cancer_phenotype(cancer_net, severity='moderate')
    cancer_runner = run_baseline_simulation(
        cancer_net,
        duration=2000,
        background_rate=5.0,
        output_file="results/cancer.h5"
    )

    # Analysis
    from analysis.basic_analysis import load_results, calculate_synchrony

    control_results = load_results("results/control.h5")
    cancer_results = load_results("results/cancer.h5")

    # Compare firing rates
    control_rates = [len(times)/2.0 for times in control_results['spikes'].values()]
    cancer_rates = [len(times)/2.0 for times in cancer_results['spikes'].values()]

    print("\n=== Comparison ===")
    print(f"Control mean rate: {np.mean(control_rates):.2f} Hz")
    print(f"Cancer mean rate: {np.mean(cancer_rates):.2f} Hz")
    print(f"Fold change: {np.mean(cancer_rates)/np.mean(control_rates):.2f}x")

    # Compare synchrony
    control_sync = calculate_synchrony(control_results['spikes'], 2000)
    cancer_sync = calculate_synchrony(cancer_results['spikes'], 2000)

    print(f"Control synchrony: {control_sync:.3f}")
    print(f"Cancer synchrony: {cancer_sync:.3f}")

# Run comparison
compare_control_vs_cancer()
```

## Key Papers for Parameter Values

### Glioma-Induced Hyperexcitability
1. **Venkataramani et al. (2019)** Nature
   - "Glutamatergic synaptic input to glioma cells drives brain tumour progression"
   - Shows increased neuronal activity in tumor microenvironment

2. **Venkatesh et al. (2019)** Nature
   - "Electrical and synaptic integration of glioma into neural circuits"
   - Documents altered synaptic properties

### Ion Channel Changes
3. **Campbell et al. (2015)** J Neurosci
   - Nav channel expression changes
   - Suggests 20-40% increase in Nav conductance

4. **Ruden & Dugan (2019)** Neuroscience
   - K+ channel dysfunction in neurotoxicity
   - 15-35% reduction in Kv channels

### Seizure-Related Changes
5. **Huberfeld et al. (2007)** Ann Neurol
   - Peritumoral tissue properties
   - GABAergic dysfunction (~30% reduction)

6. **Pallud et al. (2014)** Neuro Oncol
   - Epilepsy in low-grade gliomas
   - Network hyperexcitability patterns

### Chemotherapy Effects
7. **Lomeli et al. (2017)** Mol Neurobiol
   - Chemotherapy-induced cognitive impairment
   - Ion channel and synaptic changes

## Expected Outcomes

### Predicted Changes in Cancer Condition:

1. **Increased Firing Rates**
   - Control: 2-5 Hz average
   - Cancer: 5-12 Hz average (2-3x increase)

2. **Enhanced Synchrony**
   - Control: 0.1-0.3
   - Cancer: 0.3-0.6 (pro-epileptogenic)

3. **Burst Firing**
   - Emergence of population bursts
   - Longer burst duration

4. **Altered Oscillations**
   - Shift from gamma (30-80 Hz) dominance
   - Increase in low-frequency power

## Validating Your Model

Compare simulation results with experimental data:

1. **Firing rate increases** in peritumoral recordings
2. **Seizure susceptibility** (easier to evoke bursts)
3. **LFP power changes** (if implemented)
4. **Response to antiepileptic drugs** (can be simulated)

## Future Directions

- Add astrocyte models (glutamate buffering)
- Include inflammatory mediators (IL-1β, TNF-α effects)
- Model blood-brain barrier disruption
- Add treatment effects (AEDs, chemotherapy)
- Implement plasticity changes over time

## References

See main `README.md` and papers cited above for full reference list.
