TITLE Calcium dynamics
:
: Intracellular calcium accumulation and decay
: Based on Destexhe et al. (1994)
: Tracks submembrane calcium for calcium-dependent channels
:
: Author: NeuroV2 Project
: Date: 2025

NEURON {
    SUFFIX cadyn
    USEION ca READ ica WRITE cai
    RANGE depth, tau, cainf, cai
}

UNITS {
    (molar) = (1/liter)
    (mM) = (millimolar)
    (um) = (micron)
    (mA) = (milliamp)
    FARADAY = (faraday) (coulomb)
}

PARAMETER {
    depth = 0.1 (um)      : depth of shell for calcium accumulation
    tau = 80 (ms)         : calcium removal time constant
    cainf = 0.0001 (mM)   : resting calcium concentration
    cao = 2 (mM)          : external calcium concentration
}

STATE {
    cai (mM)
}

ASSIGNED {
    ica (mA/cm2)
    drive_channel (mM/ms)
}

INITIAL {
    cai = cainf
}

BREAKPOINT {
    SOLVE state METHOD cnexp
}

DERIVATIVE state {
    : Drive is proportional to calcium current
    : Factor of 10000 converts: (mA/cm2) * (um) / (FARADAY) / (2) -> mM/ms
    : The 2 is the valence of calcium
    drive_channel = -10000 * ica * depth / (2 * FARADAY)

    if (drive_channel <= 0) {
        drive_channel = 0
    }

    : Calcium accumulation and decay
    cai' = drive_channel + (cainf - cai) / tau
}
