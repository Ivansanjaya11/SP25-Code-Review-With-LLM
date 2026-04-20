from src.code_review_with_llm.output_objects.Analysis import Analysis
import pytest

@pytest.fixture
def analysis():
    return Analysis("1", "file.txt", "changes", "analysis")

def test_get_commit_id(analysis):
    assert analysis.get_commit_id() == "1"

def test_get_filename(analysis):
    assert analysis.get_filename() == "file.txt"

def test_get_changes(analysis):
    assert analysis.get_changes() == "changes"

def test_get_analysis(analysis):
    assert analysis.get_analysis() == "analysis"

def test_set_analysis(analysis):
    analysis.set_analysis("new analysis")
    assert analysis.get_analysis() == "new analysis"

def test_analysis_default_none():
    analysis = Analysis("1", "file.txt", "changes")
    assert analysis.get_analysis() is None
