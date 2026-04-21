from datetime import datetime
from pathlib import Path

import pytest
from src.code_review_with_llm.model.PDFGenerator import PDFGenerator
from src.code_review_with_llm.output_objects.Error import Error
from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput
from src.code_review_with_llm.output_objects.Output import Output
from src.code_review_with_llm.output_objects.PullRequestInfo import PullRequestInfo
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo
from src.code_review_with_llm.output_objects.TestCase import TestCase

@pytest.fixture
def repo_info():
    return RepositoryInfo("test-repo", "https://github.com/owner/test-repo", "owner")

@pytest.fixture
def pr_info(repo_info):
    return PullRequestInfo(1, "Fix bug", "Fixed the login bug",
                           ["abc123"], "code changes here", repo_info)

@pytest.fixture
def feedback():
    error = Error("BOUNDS_ERROR", "medium", "Index out of range", "arr[10]")
    error.set_fix_suggestion("Check length first")
    return FeedbackOutput([error], datetime(2024, 7, 15, 10, 30))

@pytest.fixture
def test_cases():
    tc = TestCase("test_login.py", Path("tests/test_login.py"))
    return [tc]

@pytest.fixture
def output(pr_info, test_cases, feedback):
    return Output(pr_info, test_cases, feedback)

@pytest.fixture
def pdf_generator(output):
    return PDFGenerator(output)

def test_create_path(pdf_generator, feedback):
    pdf_generator.create_path(feedback, 1, "test repo")

    expected_dir = Path("generated_pdf") / "2024_7"
    expected_file = "2024_7_15_10_30_test_repo_1.pdf"

    assert pdf_generator.path == expected_dir / expected_file

def test_generate(output, pdf_generator):
    pdf_generator.generate()

    assert pdf_generator.path.exists()
    assert pdf_generator.path.suffix == ".pdf"

    with open(pdf_generator.path, "rb") as f:
        content = f.read()

    assert content.startswith(b"%PDF")
