TITLE Passive leak channel
:
: Passive leak current
: Simple ohmic conductance with reversal potential
: Combines K+ leak and Cl- leak currents
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX leak
    NONSPECIFIC_CURRENT i
    RANGE g, e, i
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

PARAMETER {
    g = 0.0001 (S/cm2)    : leak conductance
    e = -70 (mV)          : leak reversal potential
}

ASSIGNED {
    v (mV)
    i (mA/cm2)
}

BREAKPOINT {
    i = g * (v - e)
}
