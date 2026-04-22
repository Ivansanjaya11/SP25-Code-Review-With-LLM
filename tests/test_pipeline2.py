import pytest
from src.code_review_with_llm.model.Pipeline2 import Pipeline2
from src.code_review_with_llm.output_objects.Output import Output


@pytest.fixture
def pipeline2():
    return Pipeline2(4, 5, 2026, 2026, True)

def test_pipeline2_run(pipeline2):
    for a_list in pipeline2.run():
        assert all(isinstance(out, Output) for out in a_list)
