import os
import pickle
import tempfile
from unittest import TestCase

import pandas as pd

from testmaker import TestLoader, TestMaker


class TestTestLoader(TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_loader = TestLoader(self.test_dir.name)

        # Generate some test data
        test_maker = TestMaker(self.test_dir.name)

        @test_maker
        def add(x, y):
            return x + y

        add(1, 2)
        add(3, 4)

        self.testcase_num = 1

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_test_case(self):
        inputs, outputs = self.test_loader.load_test_case(self.testcase_num)

        # Check inputs
        self.assertEqual(len(inputs), 2)
        for k, v in inputs.items():
            self.assertTrue(os.path.isfile(k))
            if k.endswith(".csv"):
                self.assertIsInstance(v, pd.DataFrame)
            elif k.endswith(".pkl"):
                self.assertIsNotNone(v)

        # Check outputs
        self.assertEqual(len(outputs), 1)
        self.assertTrue(
            os.path.isfile(
                os.path.join(
                    self.test_dir.name,
                    f"test_case_{self.testcase_num}",
                    "outputs",
                    "output_1.pkl",
                )
            )
        )
        self.assertIsNotNone(outputs[0])
