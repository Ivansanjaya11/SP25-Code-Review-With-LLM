import pytest
from src.code_review_with_llm.model.GeminiLLM import GeminiLLM
from src.code_review_with_llm.model.OllamaLLM import OllamaLLM
from src.code_review_with_llm.model.Pipeline3 import Pipeline3
from src.code_review_with_llm.output_objects.Analysis import Analysis
from tests.test_analysis import analysis


@pytest.fixture
def pipeline3_gemini():
    return Pipeline3("https://github.com/Ivansanjaya11/Hangman", GeminiLLM())

@pytest.fixture
def pipeline3_ollama():
    return Pipeline3("https://github.com/Ivansanjaya11/Hangman", OllamaLLM())

def test_pipeline3_run_gemini(pipeline3_gemini):
    analysis_list = pipeline3_gemini.run()
    assert all(isinstance(analysis, Analysis) for analysis in analysis_list)
    assert analysis_list

def test_pipeline3_run_ollama(pipeline3_ollama):
    analysis_list = pipeline3_ollama.run()
    assert all(isinstance(analysis, Analysis) for analysis in analysis_list)
    assert analysis_list
