TITLE Nav1.6 sodium channel
:
: Fast transient sodium current (Nav1.6)
: Based on Hu et al. (2009) and Royeck et al. (2008)
: Kinetics optimized for cortical pyramidal neurons
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX nav16
    USEION na READ ena WRITE ina
    RANGE gbar, g, ina
    GLOBAL minf, hinf, mtau, htau
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

PARAMETER {
    gbar = 0.040 (S/cm2)  : maximum conductance

    : Activation
    vhalfm = -38 (mV)     : half-activation voltage
    km = 6 (mV)           : activation slope

    : Inactivation
    vhalfh = -58 (mV)     : half-inactivation voltage
    kh = -6.7 (mV)        : inactivation slope

    : Time constants (ms)
    mtau_max = 0.5 (ms)
    htau_max = 15 (ms)
}

STATE {
    m h
}

ASSIGNED {
    v (mV)
    ena (mV)
    ina (mA/cm2)
    g (S/cm2)
    minf
    hinf
    mtau (ms)
    htau (ms)
    celsius (degC)
    qt
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = gbar * m * m * m * h
    ina = g * (v - ena)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / mtau
    h' = (hinf - h) / htau
}

INITIAL {
    qt = 2.3^((celsius-23)/10)  : Q10 temperature adjustment
    rates(v)
    m = minf
    h = hinf
}

PROCEDURE rates(v (mV)) {
    LOCAL alpha, beta

    : Activation (m)
    minf = 1 / (1 + exp(-(v - vhalfm) / km))
    alpha = 0.182 * (v + 38) / (1 - exp(-(v + 38) / 6))
    beta = 0.124 * (-v - 38) / (1 - exp((v + 38) / 6))
    mtau = (1 / (alpha + beta)) / qt
    if (mtau < 0.02) { mtau = 0.02 }
    if (mtau > mtau_max) { mtau = mtau_max }

    : Inactivation (h)
    hinf = 1 / (1 + exp(-(v - vhalfh) / kh))
    alpha = 0.024 * (v + 50) / (1 - exp(-(v + 50) / 5))
    beta = 0.0091 * (-v - 75) / (1 - exp((v + 75) / 5))
    htau = (1 / (alpha + beta)) / qt
    if (htau < 0.1) { htau = 0.1 }
    if (htau > htau_max) { htau = htau_max }
}
