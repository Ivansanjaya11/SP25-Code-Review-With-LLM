from datetime import datetime
from pathlib import Path
import pytest
import os
import json
from src.code_review_with_llm.model.JSONSaver import JSONSaver
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
def json_saver(output):
    return JSONSaver(output)

def test_save(json_saver, tmp_path):
    old_cwd = os.getcwd()

    try:
        os.chdir(tmp_path)

        json_saver.save()

        results_dir = tmp_path / "results"
        assert results_dir.exists()

        subdirs = list(results_dir.iterdir())
        assert len(subdirs) == 1

        json_file = list(subdirs[0].iterdir())[0]
        assert json_file.suffix == ".json"

        with open(json_file, "r") as f:
            data = json.load(f)

        assert "pr_info" in data
        assert "repository_info" in data
        assert "errors" in data
        assert "test_cases" in data
        assert "timestamp" in data

    finally:
        os.chdir(old_cwd)
