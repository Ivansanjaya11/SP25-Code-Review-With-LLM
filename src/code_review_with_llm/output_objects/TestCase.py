from pathlib import Path

"""
Class that contains test cases
"""
class TestCase:
    def __init__(self, test_filename: str, test_filepath: Path, test: str=""):
        self.test_filename = test_filename
        self.test_filepath = test_filepath
        self.test = test

    def get_test_filename(self) -> str:
        return self.test_filename

    def get_test_filepath(self) -> Path:
        return self.test_filepath

    def get_test(self) -> str:
        return self.test

    def set_test(self, test) -> None:
        self.test = test
