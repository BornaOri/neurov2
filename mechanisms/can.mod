TITLE N-type calcium channel
:
: High voltage-activated N-type Ca2+ current
: Based on Magee & Johnston (1995)
: Primarily localized to dendrites, critical for synaptic transmission
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX can
    USEION ca READ eca WRITE ica
    RANGE gbar, g, ica
    GLOBAL minf, hinf, mtau, htau
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

PARAMETER {
    gbar = 0.0003 (S/cm2) : maximum conductance

    : Activation
    vhalfm = -25 (mV)
    km = 6 (mV)

    : Inactivation
    vhalfh = -45 (mV)
    kh = -6.5 (mV)

    mtau_min = 0.5 (ms)
    mtau_max = 10 (ms)
    htau_min = 10 (ms)
    htau_max = 80 (ms)
}

STATE {
    m h
}

ASSIGNED {
    v (mV)
    eca (mV)
    ica (mA/cm2)
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
    g = gbar * m * m * h
    ica = g * (v - eca)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / mtau
    h' = (hinf - h) / htau
}

INITIAL {
    qt = 2.3^((celsius-23)/10)
    rates(v)
    m = minf
    h = hinf
}

PROCEDURE rates(v (mV)) {
    : Activation
    minf = 1 / (1 + exp(-(v - vhalfm) / km))
    mtau = (mtau_min + (mtau_max - mtau_min) / (1 + exp((v + 25) / 8))) / qt

    : Inactivation
    hinf = 1 / (1 + exp(-(v - vhalfh) / kh))
    htau = (htau_min + (htau_max - htau_min) / (1 + exp((v + 45) / 8))) / qt
}
