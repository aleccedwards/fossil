# Copyright (c) 2021, Alessandro Abate, Daniele Ahmed, Alec Edwards, Mirco Giacobbe, Andrea Peruffo
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pylint: disable=not-callable
from experiments.benchmarks import models
from src import domains
from src import certificate
from src import main
from src.consts import *


def test_lnn(args):
    n_vars = 2

    system = models.SecondOrderLQR

    XD = domains.Rectangle([-3.5, -3.5], [3.5, 3.5])
    XS = domains.Rectangle([-3, -3], [3, 3])
    XI = domains.Rectangle([-2, -2], [2, 2])
    XG = domains.Rectangle([-0.1, -0.1], [0.1, 0.1])
    XF = domains.Rectangle([-0.15, -0.15], [0.15, 0.15])

    SU = domains.SetMinus(XD, XS)  # Data for unsafe set
    SD = domains.SetMinus(XS, XG)  # Data for lie set
    SNF = domains.SetMinus(XD, XF)

    sets = {
        "lie": XD,
        "init": XI,
        "safe_border": XS,
        "safe": XS,
        "goal": XG,
        "final": XF,
    }
    data = {
        "lie": XD._generate_data(500),
        "init": XI._generate_data(500),
        "unsafe": SU._generate_data(500),
        "goal": XG._generate_data(500),
        "final": XF._generate_data(500),
        "not_final": SNF._generate_data(500),
    }

    # define NN parameters
    activations = [ActivationType.SOFTPLUS]
    n_hidden_neurons = [6] * len(activations)

    activations_alt = [ActivationType.SQUARE]
    n_hidden_neurons_alt = [6] * len(activations_alt)

    opts = CegisConfig(
        DOMAINS=sets,
        DATA=data,
        SYSTEM=system,
        N_VARS=n_vars,
        CERTIFICATE=CertificateType.RAR,
        TIME_DOMAIN=TimeDomain.CONTINUOUS,
        VERIFIER=VerifierType.DREAL,
        ACTIVATION=activations,
        N_HIDDEN_NEURONS=n_hidden_neurons,
        ACTIVATION_ALT=activations_alt,
        N_HIDDEN_NEURONS_ALT=n_hidden_neurons_alt,
        CEGIS_MAX_ITERS=100,
        SYMMETRIC_BELT=False,
        # VERBOSE=False,
    )

    main.run_benchmark(
        opts,
        record=args.record,
        plot=args.plot,
        concurrent=args.concurrent,
        repeat=args.repeat,
        # xrange=[-0.2, 0.2],
        # yrange=[-0.2, 0.2],
    )


if __name__ == "__main__":
    args = main.parse_benchmark_args()
    test_lnn(args)
