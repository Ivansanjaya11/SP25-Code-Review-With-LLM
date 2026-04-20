import pytest
from src.code_review_with_llm.output_objects.Error import Error

@pytest.fixture
def error():
    return Error("INFINITE_LOOP_ERROR", "high", "Loop never ends", "while True: pass")

def test_error_type(error):
    assert error.get_error_type() == "INFINITE_LOOP_ERROR"

def test_error_severity(error):
    assert error.get_error_severity_level() == "high"

def test_error_description(error):
    assert error.get_error_description() == "Loop never ends"

def test_fix_suggestion_default(error):
    assert error.get_fix_suggestion() is None

def test_code(error):
    assert error.get_code() == "while True: pass"

def test_set_fix_suggestion(error):
    error.set_fix_suggestion("new fix suggestion")
    assert error.get_fix_suggestion() == "new fix suggestion"
