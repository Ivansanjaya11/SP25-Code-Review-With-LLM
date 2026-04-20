import pytest
from src.code_review_with_llm.output_objects.Error import Error
from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput
from src.code_review_with_llm.output_objects.Output import Output
from src.code_review_with_llm.output_objects.PullRequestInfo import PullRequestInfo
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo
from src.code_review_with_llm.output_objects.TestCase import TestCase
from pathlib import Path


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
    return FeedbackOutput([error])


@pytest.fixture
def test_cases():
    tc = TestCase("test_login.py", Path("tests/test_login.py"))
    return [tc]


@pytest.fixture
def output(pr_info, test_cases, feedback):
    return Output(pr_info, test_cases, feedback)


def test_get_pr_info(output, pr_info):
    assert output.get_pr_info() == pr_info


def test_get_feedback_output(output, feedback):
    assert output.get_feedback_output() == feedback


def test_get_test_cases(output, test_cases):
    assert output.get_test_cases() == test_cases


def test_default_none_values():
    empty_output = Output()
    assert empty_output.get_pr_info() is None
    assert empty_output.get_feedback_output() is None
    assert empty_output.get_test_cases() is None


def test_str_contains_pr_id(output):
    result = str(output)
    assert "PR ID: 1" in result


def test_str_contains_title(output):
    result = str(output)
    assert "Fix bug" in result


def test_str_contains_description(output):
    result = str(output)
    assert "Fixed the login bug" in result
