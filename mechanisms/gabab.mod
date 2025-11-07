TITLE GABA-B receptor
:
: GABA-B type receptor
: Slow inhibitory synaptic current (K+ conductance)
: Based on Destexhe & Sejnowski (1995)
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    POINT_PROCESS GABAB
    RANGE tau1, tau2, e, i, g, gmax
    USEION k READ ek
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    tau1 = 50 (ms)        : rise time constant
    tau2 = 200 (ms)       : decay time constant
    e = -90 (mV)          : reversal potential (K+)
    gmax = 0.0005 (uS)    : maximum conductance
}

ASSIGNED {
    v (mV)
    ek (mV)
    i (nA)
    g (uS)
    factor
}

STATE {
    A
    B
}

INITIAL {
    LOCAL tp
    A = 0
    B = 0
    tp = (tau1 * tau2) / (tau2 - tau1) * log(tau2 / tau1)
    factor = -exp(-tp / tau1) + exp(-tp / tau2)
    factor = 1 / factor
}

BREAKPOINT {
    SOLVE state METHOD cnexp
    g = gmax * (B - A)
    i = g * (v - e)
}

DERIVATIVE state {
    A' = -A / tau1
    B' = -B / tau2
}

NET_RECEIVE(weight) {
    A = A + weight * factor
    B = B + weight * factor
}
