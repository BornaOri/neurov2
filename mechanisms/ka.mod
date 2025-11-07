TITLE A-type potassium channel (KA)
:
: Transient A-type K+ current
: Based on Hoffman et al. (1997) and Migliore et al. (1999)
: Important for dendritic excitability and spike timing
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX ka
    USEION k READ ek WRITE ik
    RANGE gbar, g, ik
    GLOBAL ainf, binf, atau, btau
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S) = (siemens)
}

PARAMETER {
    gbar = 0.015 (S/cm2)  : maximum conductance

    : Activation parameters
    vhalfa = -25 (mV)     : half-activation
    ka = 15 (mV)          : activation slope

    : Inactivation parameters
    vhalfb = -70 (mV)     : half-inactivation
    kb = -8 (mV)          : inactivation slope

    atau_max = 15 (ms)
    btau_max = 50 (ms)
}

STATE {
    a b
}

ASSIGNED {
    v (mV)
    ek (mV)
    ik (mA/cm2)
    g (S/cm2)
    ainf
    binf
    atau (ms)
    btau (ms)
    celsius (degC)
    qt
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    g = gbar * a * a * a * a * b
    ik = g * (v - ek)
}

DERIVATIVE states {
    rates(v)
    a' = (ainf - a) / atau
    b' = (binf - b) / btau
}

INITIAL {
    qt = 2.3^((celsius-23)/10)
    rates(v)
    a = ainf
    b = binf
}

PROCEDURE rates(v (mV)) {
    LOCAL alpha_a, beta_a, alpha_b, beta_b

    : Activation (a)
    ainf = 1 / (1 + exp(-(v - vhalfa) / ka))
    alpha_a = 0.2 * (v + 13.1) / (1 - exp(-(v + 13.1) / 10))
    beta_a = 0.175 * (-v - 40.1) / (1 - exp((v + 40.1) / 10))
    atau = (1 / (alpha_a + beta_a)) / qt
    if (atau < 0.1) { atau = 0.1 }
    if (atau > atau_max) { atau = atau_max }

    : Inactivation (b)
    binf = 1 / (1 + exp(-(v - vhalfb) / kb))
    alpha_b = 0.0012 * (v + 55) / (exp((v + 55) / 11) - 1)
    beta_b = 0.0012 * (-v - 55) / (exp((-v - 55) / 11) - 1)
    btau = (1 / (alpha_b + beta_b)) / qt
    if (btau < 1) { btau = 1 }
    if (btau > btau_max) { btau = btau_max }
}
