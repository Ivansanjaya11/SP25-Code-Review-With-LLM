from src.code_review_with_llm.output_objects.PullRequestInfo import PullRequestInfo
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo

import pytest

@pytest.fixture
def repo_info():
    return RepositoryInfo("test-repo", "https://github.com/owner/test-repo", "owner")

@pytest.fixture
def pr_info(repo_info):
    return PullRequestInfo(1, "Fix bug", "Fixed the login bug",
                           ["abc123"], "code changes", repo_info)

def test_get_id(pr_info):
    assert pr_info.get_id() == 1

def test_get_title(pr_info):
    assert pr_info.get_title() == "Fix bug"

def test_get_description(pr_info):
    assert pr_info.get_description() == "Fixed the login bug"

def test_get_changes(pr_info):
    assert pr_info.get_changes() == "code changes"

def test_get_commit_id_list(pr_info):
    assert pr_info.get_commit_id_list() == ["abc123"]

def test_get_repo_info(pr_info, repo_info):
    assert pr_info.get_repo_info() == repo_info

def test_get_repo_info_name(pr_info):
    assert pr_info.get_repo_info().get_repo_name() == "test-repo"

def test_get_pull_request_default_none(pr_info):
    assert pr_info.get_pull_request() is None

def test_get_pr_details(pr_info, capsys):
    pr_info.get_pr_details()
    captured = capsys.readouterr()
    assert "Fix bug" in captured.out
    assert "test-repo" in captured.out

def test_multiple_commit_ids(repo_info):
    pr = PullRequestInfo(2, "Feature", "New feature",
                         ["abc123", "def456", "ghi789"], "changes", repo_info)
    assert len(pr.get_commit_id_list()) == 3