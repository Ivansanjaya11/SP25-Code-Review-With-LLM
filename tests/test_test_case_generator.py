import pytest
from src.code_review_with_llm.model.PullRequestMiner import PullRequestMiner
from src.code_review_with_llm.model.TestCaseGenerator import TestCaseGenerator
from src.code_review_with_llm.output_objects.TestCase import TestCase

@pytest.fixture
def test_case_generator():
    return TestCaseGenerator()

@pytest.fixture
def pr_miner():
    return PullRequestMiner("https://github.com/amitt001/delegator.py")

@pytest.fixture
def pr_info_list(pr_miner):
    return pr_miner.pr_list

def test_generate(test_case_generator, pr_info_list):
    for pr_info in pr_info_list:
        assert all(isinstance(test_case, TestCase) for test_case in test_case_generator.generate(pr_info))

def test_get_test_cases(test_case_generator):
    assert all(isinstance(test_case, TestCase) for test_case in test_case_generator.get_test_cases())