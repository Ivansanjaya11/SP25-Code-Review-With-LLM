import pytest
from src.code_review_with_llm.output_objects.Error import Error
from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput


@pytest.fixture
def sample_errors():
    error1 = Error("INFINITE_LOOP_ERROR", "high", "Loop never ends", "while True: pass")
    error1.set_fix_suggestion("Add a break statement")
    error2 = Error("BOUNDS_ERROR", "medium", "Index out of range", "arr[10]")
    error2.set_fix_suggestion("Check array length")
    return [error1, error2]


@pytest.fixture
def feedback(sample_errors):
    return FeedbackOutput(sample_errors)


@pytest.fixture
def empty_feedback():
    return FeedbackOutput([])


def test_get_all_errors(feedback, sample_errors):
    assert feedback.get_all_errors() == sample_errors


def test_get_all_errors_count(feedback):
    assert len(feedback.get_all_errors()) == 2


def test_empty_feedback(empty_feedback):
    assert len(empty_feedback.get_all_errors()) == 0


def test_timestamp_exists(feedback):
    assert feedback.get_timestamp() is not None


def test_add_error(feedback):
    new_error = Error("MAGIC_NUMBER_ERROR", "low", "Magic number used", "x = 42")
    feedback.add_error(new_error)
    assert len(feedback.get_all_errors()) == 3


def test_add_error_is_last(feedback):
    new_error = Error("MAGIC_NUMBER_ERROR", "low", "Magic number used", "x = 42")
    feedback.add_error(new_error)
    assert feedback.get_all_errors()[-1].get_error_type() == "MAGIC_NUMBER_ERROR"


def test_str_contains_timestamp(feedback):
    result = str(feedback)
    assert "Timestamp:" in result


def test_str_contains_error_type(feedback):
    result = str(feedback)
    assert "INFINITE_LOOP_ERROR" in result


def test_str_contains_suggestion(feedback):
    result = str(feedback)
    assert "Add a break statement" in result
