import pytest
import json
from unittest.mock import patch, MagicMock
from src.code_review_with_llm.model.GeminiLLM import GeminiLLM
from src.code_review_with_llm.output_objects.Error import Error


@pytest.fixture
def mock_gemini():
    with patch("src.code_review_with_llm.model.GeminiLLM.genai") as mock_genai, \
         patch("src.code_review_with_llm.model.GeminiLLM.load_dotenv"), \
         patch("src.code_review_with_llm.model.GeminiLLM.os.getenv", return_value="fake-key"):
        mock_client = MagicMock()
        mock_genai.Client.return_value = mock_client
        llm = GeminiLLM()
        yield llm, mock_client


@pytest.fixture
def error_json():
    return json.dumps({"errors": [{"error_type": "BOUNDS_ERROR", "severity": "high", "description": "Out of range"}]})


@pytest.fixture
def suggestion_json():
    return json.dumps({"suggestions": [{"suggestion": "Check length first"}]})


@pytest.fixture
def analysis_json():
    return json.dumps({"analysis": "Code looks fine."})


def test_request_error(mock_gemini, error_json):
    llm, client = mock_gemini
    response = MagicMock()
    response.text = error_json
    client.models.generate_content.return_value = response

    result = llm.request_error("arr[10]")
    assert "BOUNDS_ERROR" in result


def test_request_error_calls_api(mock_gemini, error_json):
    llm, client = mock_gemini
    response = MagicMock()
    response.text = error_json
    client.models.generate_content.return_value = response

    llm.request_error("arr[10]")
    assert client.models.generate_content.called


def test_request_suggestion(mock_gemini, suggestion_json):
    llm, client = mock_gemini
    response = MagicMock()
    response.text = suggestion_json
    client.models.generate_content.return_value = response

    error = Error("BOUNDS_ERROR", "high", "Out of range", "arr[10]")
    result = llm.request_suggestion(error)
    assert result.get_fix_suggestion() == "Check length first"


def test_request_suggestion_keeps_error_type(mock_gemini, suggestion_json):
    llm, client = mock_gemini
    response = MagicMock()
    response.text = suggestion_json
    client.models.generate_content.return_value = response

    error = Error("BOUNDS_ERROR", "high", "Out of range", "arr[10]")
    result = llm.request_suggestion(error)
    assert result.get_error_type() == "BOUNDS_ERROR"


def test_request_repo_analysis(mock_gemini, analysis_json):
    llm, client = mock_gemini
    response = MagicMock()
    response.text = analysis_json
    client.models.generate_content.return_value = response

    result = llm.request_repo_analysis("print('hello')")
    assert "fine" in result


def test_retry_on_503(mock_gemini, error_json):
    llm, client = mock_gemini
    response = MagicMock()
    response.text = error_json
    client.models.generate_content.side_effect = [Exception("503 error"), response]

    with patch("src.code_review_with_llm.model.GeminiLLM.time.sleep"):
        result = llm.request_error("arr[10]")
        assert "BOUNDS_ERROR" in result


def test_retry_on_429(mock_gemini, error_json):
    llm, client = mock_gemini
    response = MagicMock()
    response.text = error_json
    client.models.generate_content.side_effect = [Exception("429 error"), response]

    with patch("src.code_review_with_llm.model.GeminiLLM.time.sleep"):
        result = llm.request_error("arr[10]")
        assert "BOUNDS_ERROR" in result


def test_fails_after_3_retries(mock_gemini):
    llm, client = mock_gemini
    client.models.generate_content.side_effect = Exception("503 error")

    with patch("src.code_review_with_llm.model.GeminiLLM.time.sleep"):
        with pytest.raises(Exception):
            llm.request_error("arr[10]")


def test_raises_other_errors(mock_gemini):
    llm, client = mock_gemini
    client.models.generate_content.side_effect = Exception("400 Bad Request")

    with pytest.raises(Exception):
        llm.request_error("arr[10]")
