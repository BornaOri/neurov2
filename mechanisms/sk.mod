TITLE Small conductance calcium-activated potassium channel (SK)
:
: SK-type Ca2+ activated K+ current
: Based on Sah & Faber (2002) and Stocker (2004)
: Critical for afterhyperpolarization and spike frequency adaptation
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX sk
    USEION k READ ek WRITE ik
    USEION ca READ cai
    RANGE gbar, g, ik
    GLOBAL zinf
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (molar) = (1/liter)
    (mM) = (millimolar)
    (S) = (siemens)
}

PARAMETER {
    gbar = 0.001 (S/cm2)  : maximum conductance
    cah = 0.0005 (mM)     : half-activation calcium concentration
    n = 4                  : Hill coefficient
    tau = 1 (ms)          : time constant for z gating
}

STATE {
    z
}

ASSIGNED {
    v (mV)
    ek (mV)
    cai (mM)
    ik (mA/cm2)
    g (S/cm2)
    zinf
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = gbar * z
    ik = g * (v - ek)
}

DERIVATIVE states {
    rates(cai)
    z' = (zinf - z) / tau
}

INITIAL {
    rates(cai)
    z = zinf
}

PROCEDURE rates(cai (mM)) {
    : Calcium-dependent activation
    : Hill equation: zinf = [Ca]^n / ([Ca]^n + K^n)
    zinf = 1 / (1 + (cah / cai)^n)
}
