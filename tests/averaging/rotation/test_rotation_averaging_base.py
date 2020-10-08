"""Tests for rotation averaging base class.

Authors: Ayush Baid
"""

import unittest

import dask
import numpy as np
from gtsam import Rot3

from averaging.rotation.dummy_rotation_averaging import DummyRotationAveraging


class TestRotationAveragingBase(unittest.TestCase):
    """Main tests for rotation averaging base class."""

    def setUp(self):
        super(TestRotationAveragingBase, self).setUp()

        self.obj = DummyRotationAveraging()

    def test_computation_graph(self):
        """Test the dask computation graph execution using a valid collection
        of relative poses."""

        num_poses = 3

        iRj_dict = {
            (0, 1): Rot3.RzRyRx(0, 30*np.pi/180, 0),
            (1, 2): Rot3.RzRyRx(0, 0, 20*np.pi/180),
        }

        # use the normal API for rotation averaging
        normal_result = self.obj.run(num_poses, iRj_dict)

        # use dask's computation graph
        computation_graph = self.obj.create_computation_graph(
            num_poses,
            dask.delayed(iRj_dict)
        )

        with dask.config.set(scheduler='single-threaded'):
            dask_result = dask.compute(computation_graph)[0]

        # compare the two entries
        for idx in range(1, num_poses):
            self.assertTrue(normal_result[0].between(normal_result[idx]).equals(
                dask_result[0].between(dask_result[idx]), 1e-5))
