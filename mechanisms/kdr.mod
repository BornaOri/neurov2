TITLE Delayed rectifier potassium channel (Kdr)
:
: Delayed rectifier K+ current
: Based on Korngreen & Sakmann (2000) and Migliore et al. (1999)
: Standard in cortical pyramidal neurons
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX kdr
    USEION k READ ek WRITE ik
    RANGE gbar, g, ik
    GLOBAL ninf, ntau
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

PARAMETER {
    gbar = 0.010 (S/cm2)  : maximum conductance

    : Activation parameters
    vhalfn = -15 (mV)     : half-activation voltage
    kn = 13 (mV)          : activation slope
    ntau_max = 15 (ms)    : maximum time constant
}

STATE {
    n
}

ASSIGNED {
    v (mV)
    ek (mV)
    ik (mA/cm2)
    g (S/cm2)
    ninf
    ntau (ms)
    celsius (degC)
    qt
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = gbar * n * n * n * n
    ik = g * (v - ek)
}

DERIVATIVE states {
    rates(v)
    n' = (ninf - n) / ntau
}

INITIAL {
    qt = 2.3^((celsius-23)/10)  : Q10 temperature adjustment
    rates(v)
    n = ninf
}

PROCEDURE rates(v (mV)) {
    LOCAL alpha, beta

    : Activation (n)
    ninf = 1 / (1 + exp(-(v - vhalfn) / kn))

    alpha = 0.028 * (v + 25) / (1 - exp(-(v + 25) / 10))
    beta = 0.0175 * (-v - 25) / (1 - exp((v + 25) / 10))

    ntau = (1 / (alpha + beta)) / qt
    if (ntau < 0.1) { ntau = 0.1 }
    if (ntau > ntau_max) { ntau = ntau_max }
}
