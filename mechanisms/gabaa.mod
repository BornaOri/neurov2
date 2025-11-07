TITLE GABA-A receptor
:
: GABA-A type receptor
: Fast inhibitory synaptic current
: Based on Destexhe et al. (1998)
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    POINT_PROCESS GABAA
    RANGE tau1, tau2, e, i, g, gmax
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    tau1 = 0.5 (ms)       : rise time constant
    tau2 = 10 (ms)        : decay time constant
    e = -70 (mV)          : reversal potential (chloride)
    gmax = 0.001 (uS)     : maximum conductance
}

ASSIGNED {
    v (mV)
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
