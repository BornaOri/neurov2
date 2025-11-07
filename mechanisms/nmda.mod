TITLE NMDA receptor with magnesium block
:
: NMDA-type glutamate receptor
: Slow excitatory synaptic current with voltage-dependent Mg2+ block
: Based on Jahr & Stevens (1990) and Destexhe et al. (1998)
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    POINT_PROCESS NMDA
    RANGE tau1, tau2, e, i, g, gmax
    RANGE mg, mgblock
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
    (mM) = (millimolar)
}

PARAMETER {
    tau1 = 2 (ms)         : rise time constant
    tau2 = 50 (ms)        : decay time constant
    e = 0 (mV)            : reversal potential
    gmax = 0.001 (uS)     : maximum conductance
    mg = 1 (mM)           : external magnesium concentration
}

ASSIGNED {
    v (mV)
    i (nA)
    g (uS)
    factor
    mgblock
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
    mgblock = 1 / (1 + exp(-0.062 * v) * (mg / 3.57))
    g = gmax * (B - A) * mgblock
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
