import pytest
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo
from src.code_review_with_llm.output_objects.Analysis import Analysis


@pytest.fixture
def repo_info():
    return RepositoryInfo("test-repo", "https://github.com/owner/test-repo", "owner")


@pytest.fixture
def repo_info_full():
    return RepositoryInfo(
        "test-repo",
        "https://github.com/owner/test-repo",
        "owner",
        branches_names=["main", "dev"],
        commit_id_list=["abc123", "def456"],
    )


def test_get_repo_name(repo_info):
    assert repo_info.get_repo_name() == "test-repo"


def test_get_repo_url(repo_info):
    assert repo_info.get_repo_url() == "https://github.com/owner/test-repo"


def test_get_repo_owner(repo_info):
    assert repo_info.get_repo_owner() == "owner"


def test_default_branches_empty(repo_info):
    assert repo_info.get_branches_names() == []


def test_default_commit_id_list_none(repo_info):
    assert repo_info.get_commit_id_list() is None


def test_default_analysis_list_none(repo_info):
    assert repo_info.get_analysis_list() is None


def test_default_repo_details_empty(repo_info):
    assert repo_info.get_repo_details() == ""


def test_full_branches(repo_info_full):
    assert repo_info_full.get_branches_names() == ["main", "dev"]


def test_full_commit_ids(repo_info_full):
    assert repo_info_full.get_commit_id_list() == ["abc123", "def456"]


def test_set_branches_names(repo_info):
    repo_info.set_branches_names(["main", "feature"])
    assert repo_info.get_branches_names() == ["main", "feature"]


def test_set_repo_description(repo_info):
    repo_info.set_repo_description("A test repository")
    assert repo_info.get_repo_details() == "A test repository"


def test_set_commit_id_list(repo_info):
    repo_info.set_commit_id_list(["111", "222", "333"])
    assert repo_info.get_commit_id_list() == ["111", "222", "333"]


def test_set_analysis_list(repo_info):
    analysis1 = Analysis("abc123", "main.py", "print('hello')")
    analysis2 = Analysis("def456", "utils.py", "def helper(): pass")
    repo_info.set_analysis_list([analysis1, analysis2])
    assert len(repo_info.get_analysis_list()) == 2


def test_set_analysis_list_content(repo_info):
    analysis = Analysis("abc123", "main.py", "print('hello')")
    repo_info.set_analysis_list([analysis])
    assert repo_info.get_analysis_list()[0].get_filename() == "main.py"
