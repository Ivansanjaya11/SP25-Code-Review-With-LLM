import pytest
from src.code_review_with_llm.model.GeminiLLM import GeminiLLM
from src.code_review_with_llm.model.OllamaLLM import OllamaLLM
from src.code_review_with_llm.model.Pipeline1 import Pipeline1
from src.code_review_with_llm.output_objects.Output import Output


@pytest.fixture
def pipeline1_gemini():
    return Pipeline1("https://github.com/amitt001/delegator.py", [80], GeminiLLM(), True)

@pytest.fixture
def pipeline1_ollama():
    return Pipeline1("https://github.com/amitt001/delegator.py", [80], OllamaLLM(), True)

def test_pipeline1_run_gemini(pipeline1_gemini):
    assert all(isinstance(out, Output) for out in pipeline1_gemini.run())

def test_pipeline1_run_ollama(pipeline1_ollama):
    assert all(isinstance(out, Output) for out in pipeline1_ollama.run())
