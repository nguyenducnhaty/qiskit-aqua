# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

""" Test Cplex Ising """

from test.optimization import QiskitOptimizationTestCase
import numpy as np

from qiskit.aqua import aqua_globals
from qiskit.optimization.ising import max_cut
from qiskit.optimization.ising.common import random_graph
from qiskit.aqua.algorithms.classical.cplex.cplex_ising import CPLEX_Ising


class TestCplexIsing(QiskitOptimizationTestCase):
    """Cplex Ising tests."""

    def setUp(self):
        super().setUp()
        aqua_globals.random_seed = 8123179
        self.w = random_graph(4, edge_prob=0.5, weight_range=10)
        self.qubit_op, self.offset = max_cut.get_operator(self.w)

    def test_cplex_ising(self):
        """ cplex ising test """
        try:
            algo = CPLEX_Ising(self.qubit_op, display=0)
            result = algo.run()
            self.assertEqual(result['energy'], -20.5)
            x_dict = result['x_sol']
            x = np.array([x_dict[i] for i in sorted(x_dict.keys())])
            np.testing.assert_array_equal(
                max_cut.get_graph_solution(x), [1, 0, 1, 1])
            self.assertEqual(max_cut.max_cut_value(x, self.w), 24)
        except NameError as ex:
            self.skipTest(str(ex))
