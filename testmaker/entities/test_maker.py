import os

import cloudpickle
import pandas as pd

from testmaker.utils.convert_args_to_kwargs import convert_args_to_kwargs

STORE_FORMAT_PICKLE = "pickle"
STORE_FORMAT_CSV = "csv"


class TestMaker:
    def __init__(self, testcase_folder, store_format=STORE_FORMAT_PICKLE):
        self.testcase_folder = testcase_folder
        self.testcase_num = 0
        self.store_format = store_format

    def store(self, data, file_path):
        if isinstance(data, pd.DataFrame) and self.store_format == STORE_FORMAT_CSV:
            data.to_csv(file_path + ".csv", index=False)
        else:
            with open(file_path + ".pkl", "wb") as f:
                cloudpickle.dump(data, f)

    def __call__(self, func):
        function_name = func.__name__

        def wrapper(*args, **kwargs):
            self.testcase_num += 1

            input_path = os.path.join(
                self.testcase_folder, f"{function_name}__{self.testcase_num}", "inputs"
            )
            output_path = os.path.join(
                self.testcase_folder, f"{function_name}__{self.testcase_num}", "outputs"
            )
            os.makedirs(input_path, exist_ok=True)
            os.makedirs(output_path, exist_ok=True)
            converted_kwargs = convert_args_to_kwargs(func, *args, **kwargs)

            is_run_from_test_runner = converted_kwargs.pop(
                "testmaker_run_from_test_runner", False
            )
            if (
                not is_run_from_test_runner
            ):  # If the function is not run from test runner, then we don't need to store the output
                for k, v in converted_kwargs.items():
                    self.store(v, os.path.join(input_path, k))
                    # input must be save before the function is executed, because the function may change the input
            # Execute function and save output
            result = func(**converted_kwargs)
            if (
                not is_run_from_test_runner
            ):  # If the function is not run from test runner, then we don't need to store the output
                original_type = type(result)
                if type(result) not in (tuple, list):
                    result = [result]
                for i, out in enumerate(result):
                    self.store(out, os.path.join(output_path, f"output_{i+1}"))
                if original_type not in (tuple, list):
                    result = result[0]
            return result

        wrapper.__name__ = function_name
        return wrapper
