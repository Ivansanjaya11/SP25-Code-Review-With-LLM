from github import Github
from src.code_review_with_llm.model.PullRequestMiner import PullRequestMiner
import pytest
from src.code_review_with_llm.output_objects.PullRequestInfo import PullRequestInfo

@pytest.fixture
def pr_miner():
    return PullRequestMiner("https://github.com/amitt001/delegator.py")

def test_set_up_github_api(pr_miner):
    assert isinstance(pr_miner.g, Github)

def test_mine_pr(pr_miner):
    assert all(isinstance(pr_info, PullRequestInfo) for pr_info in pr_miner.pr_list)

def test_get_pull_request_info_list(pr_miner):
    assert all(isinstance(pr_info, PullRequestInfo) for pr_info in pr_miner.get_pull_request_info_list())
