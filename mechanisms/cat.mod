TITLE T-type calcium channel
:
: Low voltage-activated T-type Ca2+ current
: Based on Destexhe et al. (1998) and Huguenard & McCormick (1992)
: Important for burst firing and subthreshold oscillations
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX cat
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
    gbar = 0.0002 (S/cm2) : maximum conductance

    : Activation (low threshold)
    vhalfm = -52 (mV)
    km = 7.4 (mV)

    : Inactivation
    vhalfh = -80 (mV)
    kh = -5 (mV)

    mtau_min = 0.5 (ms)
    mtau_max = 5 (ms)
    htau_min = 10 (ms)
    htau_max = 50 (ms)
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
    : Activation (activated at low voltages)
    minf = 1 / (1 + exp(-(v - vhalfm) / km))
    mtau = (mtau_min + (mtau_max - mtau_min) / (1 + exp((v + 60) / 7))) / qt

    : Inactivation
    hinf = 1 / (1 + exp(-(v - vhalfh) / kh))
    htau = (htau_min + (htau_max - htau_min) / (1 + exp((v + 80) / 7))) / qt
}
