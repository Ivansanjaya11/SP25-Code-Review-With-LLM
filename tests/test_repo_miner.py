from github import Github
import pytest
from src.code_review_with_llm.model.RepoMiner import RepoMiner
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo

@pytest.fixture
def repo_miner():
    return RepoMiner("https://github.com/amitt001/delegator.py")

def test_set_up_github_api(repo_miner):
    assert isinstance(repo_miner.g, Github)

def test_mine_repo(repo_miner):
    assert isinstance(repo_miner.repository_info, RepositoryInfo)

def test_get_pull_request_info_list(repo_miner):
    assert isinstance(repo_miner.get_repository_info(), RepositoryInfo)
