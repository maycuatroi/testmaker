import glob
import shutil

import cloudpickle

from testmaker import TestMaker


def test_testmaker_class_decorator():
    @TestMaker("test_cases")
    def multiply(a, b):
        return a * b

    for i in range(5):
        multiply(i, i + 1)

        # Load test cases and verify results
    for i in range(1, 6):
        with open(f"test_cases/test_case_{i}/inputs/a.pkl", "rb") as f:
            a = cloudpickle.load(f)
        with open(f"test_cases/test_case_{i}/inputs/b.pkl", "rb") as f:
            b = cloudpickle.load(f)
        with open(f"test_cases/test_case_{i}/outputs/output_1.pkl", "rb") as f:
            expected = cloudpickle.load(f)
        result = multiply(a, b)
        assert result == expected, f"Test case {i} failed: {result} != {expected}"
    print("All test cases passed.")
    # Clean up test cases
    files = glob.glob("test_cases/*")
    for f in files:
        shutil.rmtree(f)
