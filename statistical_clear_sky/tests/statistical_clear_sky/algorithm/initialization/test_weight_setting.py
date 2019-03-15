import unittest
import os
import numpy as np
import cvxpy as cvx
from statistical_clear_sky.algorithm.initialization.weight_setting\
 import WeightSetting
from statistical_clear_sky.solver_type import SolverType

class TestWeightSetting(unittest.TestCase):

    def test_obtain_weights(self):

        # Data from Example_02 Jupyter notebook.
        # From 100th to 103th element of outer array,
        # first 4 elements of inner array.
        power_signals_d = np.array([[3.65099996e-01, 0.00000000e+00,
                                     0.00000000e+00, 2.59570003e+00],
                                    [6.21100008e-01, 0.00000000e+00,
                                     0.00000000e+00, 2.67740011e+00],
                                    [8.12500000e-01, 0.00000000e+00,
                                     0.00000000e+00, 2.72729993e+00],
                                    [9.00399983e-01, 0.00000000e+00,
                                     0.00000000e+00, 2.77419996e+00]])

        # Data from Example_02 Jupyter notebook.
        # From 100th to 103th element of array.
        #expected_weights = np.array([0.0, 0.97870261, 0.93385772, 0.0])
        # TODO: Get better test data, so that some of the values are > 0.6.
        #       Note: Data must be smaller than the data from Example_02,
        #             since the default ECOS solver fails with large data.
        expected_weights = np.array([0.0, 0.0, 0.0, 0.0])

        weight_setting = WeightSetting()
        actual_weights = weight_setting.obtain_weights(power_signals_d)

        np.testing.assert_array_equal(actual_weights, expected_weights)

    def test_obtain_weights_with_example_02_data(self):

        input_power_signals_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         "../../fixtures/power_signals_d_1.csv"))
        with open(input_power_signals_file_path) as file:
            power_signals_d = np.loadtxt(file, delimiter=',')

        weights_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         "../../fixtures/weights_1.csv"))
        with open(weights_file_path) as file:
            expected_weights = np.loadtxt(file, delimiter=',')

        weight_setting = WeightSetting(solver_type=SolverType.mosek)
        try:
            actual_weights = weight_setting.obtain_weights(power_signals_d)
        except cvx.SolverError:
            self.skipTest("This test uses MOSEK solver"
                + "because default ECOS solver fails with large data. "
                + "Unless MOSEK is installed, this test fails.")
        else:
            np.testing.assert_array_equal(actual_weights, expected_weights)