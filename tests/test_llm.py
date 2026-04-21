import pytest
from src.code_review_with_llm.model.LLM import LLM


@pytest.fixture
def llm():
    return LLM("test-model")


@pytest.fixture
def single_error_json():
    return '{"errors": [{"error_type": "BOUNDS_ERROR", "severity": "high", "description": "Index out of range"}]}'


@pytest.fixture
def multiple_errors_json():
    return '{"errors": [{"error_type": "BOUNDS_ERROR", "severity": "high", "description": "Index out of range"}, {"error_type": "INFINITE_LOOP_ERROR", "severity": "medium", "description": "Loop never ends"}]}'


@pytest.fixture
def empty_errors_json():
    return '{"errors": []}'


@pytest.fixture
def sample_code():
    return "arr[10]"


def test_parse_single_error_count(llm, single_error_json, sample_code):
    errors = llm.parse_error_response(single_error_json, sample_code)
    assert len(errors) == 1


def test_parse_single_error_type(llm, single_error_json, sample_code):
    errors = llm.parse_error_response(single_error_json, sample_code)
    assert errors[0].get_error_type() == "BOUNDS_ERROR"


def test_parse_single_error_severity(llm, single_error_json, sample_code):
    errors = llm.parse_error_response(single_error_json, sample_code)
    assert errors[0].get_error_severity_level() == "high"


def test_parse_single_error_description(llm, single_error_json, sample_code):
    errors = llm.parse_error_response(single_error_json, sample_code)
    assert errors[0].get_error_description() == "Index out of range"


def test_parse_single_error_code(llm, single_error_json, sample_code):
    errors = llm.parse_error_response(single_error_json, sample_code)
    assert errors[0].get_code() == "arr[10]"


def test_parse_multiple_errors_count(llm, multiple_errors_json, sample_code):
    errors = llm.parse_error_response(multiple_errors_json, sample_code)
    assert len(errors) == 2


def test_parse_multiple_errors_types(llm, multiple_errors_json, sample_code):
    errors = llm.parse_error_response(multiple_errors_json, sample_code)
    assert errors[0].get_error_type() == "BOUNDS_ERROR"
    assert errors[1].get_error_type() == "INFINITE_LOOP_ERROR"


def test_parse_empty_errors(llm, empty_errors_json, sample_code):
    errors = llm.parse_error_response(empty_errors_json, sample_code)
    assert len(errors) == 0


def test_parse_none_response(llm, sample_code):
    errors = llm.parse_error_response("NONE", sample_code)
    assert len(errors) == 0


def test_parse_fix_suggestion_default_none(llm, single_error_json, sample_code):
    errors = llm.parse_error_response(single_error_json, sample_code)
    assert errors[0].get_fix_suggestion() is None


def test_llm_model_name(llm):
    assert llm.model == "test-model"


def test_llm_prompts_loaded(llm):
    assert llm.system_prompt_error is not None


def test_llm_available_error_types(llm):
    assert "INFINITE_LOOP_ERROR" in llm.available_error_types


def test_llm_available_error_types_no_others(llm):
    assert "OTHERS" not in llm.available_error_types
