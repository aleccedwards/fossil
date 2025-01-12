# Copyright (c) 2021, Alessandro Abate, Daniele Ahmed, Alec Edwards, Mirco Giacobbe, Andrea Peruffo
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pylint: disable=not-callable
import numpy
import torch
import timeit
from src.cegis import Cegis
from experiments.benchmarks.benchmark_ctrl import ctrllyap_lorenz_sys


from src.consts import *
from src.plots.plot_lyap import plot_lyce
import numpy as np


def test_lnn():
    # TEST for Control Lyapunov
    # pass the ctrl parameters from here (i.e. the main)
    benchmark = ctrllyap_lorenz_sys
    n_vars = 3
    system = benchmark

    # define NN parameters
    lyap_activations = [ActivationType.SQUARE]
    lyap_hidden_neurons = [10] * len(lyap_activations)

    # ctrl params
    n_ctrl_inputs = 3

    start = timeit.default_timer()
    opts = CegisConfig(
        N_VARS=n_vars,
        CERTIFICATE=CertificateType.LYAPUNOV,
        LLO=True,
        TIME_DOMAIN=TimeDomain.CONTINUOUS,
        VERIFIER=VerifierType.DREAL,
        ACTIVATION=lyap_activations,
        SYSTEM=system,
        N_HIDDEN_NEURONS=lyap_hidden_neurons,
        CTRLAYER=[10, n_ctrl_inputs],
        CTRLACTIVATION=[ActivationType.LINEAR],
    )
    c = Cegis(opts)
    state, vars, f, iters = c.solve()
    stop = timeit.default_timer()
    print("Elapsed Time: {}".format(stop - start))

    # plotting -- only for 2-d systems
    if len(vars) == 2:
        plot_lyce(
            np.array(vars), state[CegisStateKeys.V], state[CegisStateKeys.V_dot], f
        )


if __name__ == "__main__":
    torch.manual_seed(167)
    test_lnn()
