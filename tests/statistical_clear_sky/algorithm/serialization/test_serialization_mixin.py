import unittest
import numpy as np
import tempfile
import shutil
import os
from statistical_clear_sky.algorithm.iterative_clear_sky\
import IterativeClearSky

class TestSerializationMixin(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.mkdtemp()
        self.filepath = os.path.join(self.temp_directory, 'state_data.json')

    def tearDown(self):
        shutil.rmtree(self.temp_directory)

    def test_serialization(self):

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
        rank_k = 4

        original_iterative_clear_sky = IterativeClearSky(power_signals_d,
                                   rank_k=rank_k, auto_fix_time_shifts=False)

        original_iterative_clear_sky.save_instance(self.filepath)

        deserialized_iterative_clear_sky = IterativeClearSky.load_instance(
            self.filepath)

        np.testing.assert_array_equal(deserialized_iterative_clear_sky.
                                      _power_signals_d,
                                      original_iterative_clear_sky.
                                      _power_signals_d)