import pytest
from src.code_review_with_llm.model.Pipeline import Pipeline


def test_pipeline_output_list_empty():
    pipeline = Pipeline()
    assert pipeline.output_list == []


def test_pipeline_run_returns_none():
    pipeline = Pipeline()
    assert pipeline.run() is None
