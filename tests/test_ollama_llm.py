import pytest
import json
from unittest.mock import patch, MagicMock
from src.code_review_with_llm.model.OllamaLLM import OllamaLLM
from src.code_review_with_llm.output_objects.Error import Error


@pytest.fixture
def mock_ollama():
    with patch("src.code_review_with_llm.model.OllamaLLM.ollama") as mock_mod:
        mock_client = MagicMock()
        mock_mod.Client.return_value = mock_client
        llm = OllamaLLM()
        yield llm, mock_client


@pytest.fixture
def error_response():
    return {"message": {"content": json.dumps(
        {"errors": [{"error_type": "INFINITE_LOOP_ERROR", "severity": "high", "description": "Loop never ends"}]}
    )}}


@pytest.fixture
def suggestion_response():
    return {"message": {"content": json.dumps(
        {"suggestions": [{"suggestion": "Add counter increment"}]}
    )}}


@pytest.fixture
def analysis_response():
    return {"message": {"content": json.dumps(
        {"analysis": "Code shows consistent patterns."}
    )}}


def test_request_error(mock_ollama, error_response):
    llm, client = mock_ollama
    client.chat.return_value = error_response

    result = llm.request_error("while True: pass")
    assert "INFINITE_LOOP_ERROR" in result


def test_request_error_calls_chat(mock_ollama, error_response):
    llm, client = mock_ollama
    client.chat.return_value = error_response

    llm.request_error("while True: pass")
    assert client.chat.called


def test_request_error_uses_model(mock_ollama, error_response):
    llm, client = mock_ollama
    client.chat.return_value = error_response

    llm.request_error("while True: pass")
    call_args = client.chat.call_args
    assert call_args.kwargs["model"] == "llama3:latest"


def test_request_suggestion(mock_ollama, suggestion_response):
    llm, client = mock_ollama
    client.chat.return_value = suggestion_response

    error = Error("INFINITE_LOOP_ERROR", "high", "Loop never ends", "while True: pass")
    result = llm.request_suggestion(error)
    assert result.get_fix_suggestion() == "Add counter increment"


def test_request_suggestion_keeps_error_info(mock_ollama, suggestion_response):
    llm, client = mock_ollama
    client.chat.return_value = suggestion_response

    error = Error("INFINITE_LOOP_ERROR", "high", "Loop never ends", "while True: pass")
    result = llm.request_suggestion(error)
    assert result.get_error_type() == "INFINITE_LOOP_ERROR"
    assert result.get_error_severity_level() == "high"


def test_request_repo_analysis(mock_ollama, analysis_response):
    llm, client = mock_ollama
    client.chat.return_value = analysis_response

    result = llm.request_repo_analysis("print('hello')")
    assert "consistent" in result


def test_default_model():
    with patch("src.code_review_with_llm.model.OllamaLLM.ollama") as mock_mod:
        mock_mod.Client.return_value = MagicMock()
        llm = OllamaLLM()
        assert llm.model == "llama3:latest"


def test_custom_model():
    with patch("src.code_review_with_llm.model.OllamaLLM.ollama") as mock_mod:
        mock_mod.Client.return_value = MagicMock()
        llm = OllamaLLM(model="codellama")
        assert llm.model == "codellama"
