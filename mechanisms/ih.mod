TITLE Hyperpolarization-activated cation current (Ih/HCN)
:
: Ih current (HCN channels)
: Based on Magee (1998) and Kole et al. (2006)
: Critical for dendritic integration and resonance
: Mixed Na+/K+ conductance with reversal ~-30 mV
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX ih
    NONSPECIFIC_CURRENT i
    RANGE gbar, g, i, eh
    GLOBAL linf, ltau
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

PARAMETER {
    gbar = 0.0001 (S/cm2) : maximum conductance
    eh = -30 (mV)         : reversal potential (mixed cation)

    : Activation parameters
    vhalf = -90 (mV)      : half-activation voltage
    k = 8.5 (mV)          : activation slope

    : Time constant parameters
    tau_min = 20 (ms)     : minimum tau
    tau_max = 1000 (ms)   : maximum tau
}

STATE {
    l
}

ASSIGNED {
    v (mV)
    i (mA/cm2)
    g (S/cm2)
    linf
    ltau (ms)
    celsius (degC)
    qt
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = gbar * l
    i = g * (v - eh)
}

DERIVATIVE states {
    rates(v)
    l' = (linf - l) / ltau
}

INITIAL {
    qt = 4.5^((celsius-33)/10)  : Q10 = 4.5 for Ih
    rates(v)
    l = linf
}

PROCEDURE rates(v (mV)) {
    : Activation is voltage-dependent and slow
    linf = 1 / (1 + exp((v - vhalf) / k))

    : Voltage-dependent time constant (slower at intermediate voltages)
    ltau = (tau_min + (tau_max - tau_min) * exp(-0.033 * (v + 75))) / qt

    if (ltau < tau_min) { ltau = tau_min }
    if (ltau > tau_max) { ltau = tau_max }
}
