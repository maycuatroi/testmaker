import os
import pickle
from glob import glob

import pandas as pd


class TestLoader:
    def __init__(self, testcase_folder, function_name):
        self.testcase_folder = testcase_folder
        self.function_name = function_name

    def _load_file(self, file_path):
        if file_path.endswith(".pkl"):
            return self.__load_pickle(file_path)
        elif file_path.endswith(".csv"):
            return self.__load_csv(file_path)
        else:
            raise ValueError("File type not supported")

    def load_test_case(self, testcase_num):
        input_path = os.path.join(
            self.testcase_folder, f"{self.function_name}__{testcase_num}", "inputs"
        )
        output_path = os.path.join(
            self.testcase_folder, f"{self.function_name}__{testcase_num}", "outputs"
        )
        inputs = {}
        outputs = []

        for path in [input_path, output_path]:
            for file_name in glob(f"{path}/*"):
                if os.path.isfile(file_name):
                    if path == input_path:
                        key = os.path.basename(file_name).split(".")[0]
                        inputs[key] = self._load_file(file_name)
                    else:
                        outputs.append(self._load_file(file_name))
        return inputs, outputs

    def __load_pickle(self, file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)

    def __load_csv(self, file_path):
        return pd.read_csv(file_path)
