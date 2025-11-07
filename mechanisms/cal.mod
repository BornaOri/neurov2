TITLE L-type calcium channel
:
: High voltage-activated L-type Ca2+ current
: Based on Reuveni et al. (1993) and Markram et al. (2015)
: Important for calcium influx during bursting and plateau potentials
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX cal
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
    gbar = 0.0005 (S/cm2) : maximum conductance

    : Activation
    vhalfm = -20 (mV)
    km = 7 (mV)

    : Inactivation
    vhalfh = -40 (mV)
    kh = -7 (mV)

    mtau_min = 1 (ms)
    mtau_max = 40 (ms)
    htau_min = 20 (ms)
    htau_max = 200 (ms)
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
    mtau = (mtau_min + (mtau_max - mtau_min) / (1 + exp((v + 20) / 10))) / qt

    : Inactivation
    hinf = 1 / (1 + exp(-(v - vhalfh) / kh))
    htau = (htau_min + (htau_max - htau_min) / (1 + exp((v + 40) / 10))) / qt
}
