from src.code_review_with_llm.output_objects.TestCase import TestCase
from pathlib import Path
import pytest

@pytest.fixture
def test_case():
    return TestCase("filename", Path("tests/filepath"), "test")

def test_get_test_filename(test_case):
    assert test_case.get_test_filename() == "filename"

def test_get_test_filepath(test_case):
    assert test_case.get_test_filepath() == Path("tests/filepath")

def test_get_test(test_case):
    assert test_case.get_test() == "test"

def test_set_test(test_case):
    test_case.set_test("new test")
    assert test_case.get_test() == "new test"

def test_default_test_empty():
    tc = TestCase("filename", Path("tests/filename"))
    assert tc.get_test() == ""