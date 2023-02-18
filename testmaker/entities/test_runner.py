import glob
import logging
import os

import pandas as pd
from tqdm import tqdm

from testmaker import TestLoader


class TestRunner:
    def __init__(self, testcase_folder=None, function=None, function_name=None):
        self.testcase_folder = testcase_folder or "test-maker"
        self.function_name = function_name
        self.function_to_test = function
        if function is not None:
            self.function_name = function.__name__

        self.loader = TestLoader(
            testcase_folder=self.testcase_folder, function_name=self.function_name
        )

    def load_test_case(self, testcase_num):
        return self.loader.load_test_case(testcase_num)

    def get_test_folders(self):
        folders=  glob.glob(f"{self.testcase_folder}/*__*")
        folders = [folder for folder in folders if os.path.basename(folder).split("__")[0] == self.function_name]
        return folders
    def __test_case_generator(self):
        test_folders = self.get_test_folders()
        for folder in test_folders:
            test_num = folder.split("__")[-1]
            test_case = self.load_test_case(test_num)
            yield test_num,*test_case
    def load_all_test_cases(self):
        test_case_count  = len(self.get_test_folders())
        return test_case_count,self.__test_case_generator()


    def run_all_test_cases(self):
        # If no testcase_num is provided, run all test cases
        test_case_count, test_cases_generator = self.load_all_test_cases()
        logging.info(f"Running {test_case_count} test cases")
        progress_bar = tqdm(test_cases_generator,total=test_case_count,desc="Running test cases")
        for test_index,inputs, results in progress_bar:
            self.run_test_case(inputs, results)
            message=  f"Test case {test_index} passed"
            logging.info(message)
            progress_bar.set_description(message)

        return True

    def run_test_case(self, inputs, results):
        # run function to get outputs, and compare to expected results
        outputs = self.function_to_test(testmaker_run_from_test_runner=True, **inputs)
        if not isinstance(outputs, list):
            outputs = [outputs]
        for output, result in zip(outputs, results):
            if isinstance(output, pd.DataFrame) or isinstance(output, pd.Series):
                assert output.equals(
                    result
                ), f"Output {output} does not match expected result {result}"
            else:
                assert (
                    output == result
                ), f"Output {output} does not match expected result {result}"
        return True
