# Copyright (c) 2021, Alessandro Abate, Daniele Ahmed, Alec Edwards, Mirco Giacobbe, Andrea Peruffo
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import timeit

# pylint: disable=not-callable
import torch

from src import domains
from src import certificate
from src import main
from experiments.benchmarks import models
from experiments.benchmarks.models import SecondOrder
from src.consts import *


def test_lnn(args):
    ###########################################
    ###
    #############################################
    n_vars = 2

    ol_system = SecondOrder
    system = models.GeneralClosedLoopModel.prepare_from_open(ol_system())

    XD = domains.Rectangle([-1.5, -1.5], [1.5, 1.5])
    XS = domains.Rectangle([-1, -1], [1, 1])
    XI = domains.Rectangle([-0.5, -0.5], [0.5, 0.5])
    XG = domains.Rectangle([-0.05, -0.05], [0.05, 0.05])

    SU = domains.SetMinus(XD, XS)  # Data for unsafe set
    SD = domains.SetMinus(XS, XG)  # Data for lie set

    sets = {
        certificate.XD: XD,
        certificate.XI: XI,
        certificate.XS_BORDER: XS,
        certificate.XS: XS,
        certificate.XG: XG,
    }
    data = {
        certificate.XD: XD._generate_data(1000),
        certificate.XI: XI._generate_data(1000),
        certificate.XU: SU._generate_data(1000),
    }
    # define NN parameters
    activations = [ActivationType.SQUARE]
    n_hidden_neurons = [8] * len(activations)

    opts = CegisConfig(
        DOMAINS=sets,
        DATA=data,
        SYSTEM=system,
        N_VARS=n_vars,
        CERTIFICATE=CertificateType.RWS,
        TIME_DOMAIN=TimeDomain.CONTINUOUS,
        VERIFIER=VerifierType.DREAL,
        ACTIVATION=activations,
        N_HIDDEN_NEURONS=n_hidden_neurons,
        CEGIS_MAX_ITERS=25,
        CTRLAYER=[8, 1],
        CTRLACTIVATION=[ActivationType.LINEAR],
    )

    main.run_benchmark(
        opts,
        record=args.record,
        plot=args.plot,
        concurrent=args.concurrent,
        repeat=args.repeat,
    )


if __name__ == "__main__":
    args = main.parse_benchmark_args()
    test_lnn(args)
