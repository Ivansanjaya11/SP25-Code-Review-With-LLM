from PullRequestInfo import PullRequestInfo
from FeedbackOutput import FeedbackOutput
from TestCase import TestCase

class Output:
    def __init__(self, pr_info: PullRequestInfo, test_cases: list[TestCase], feedback_output: FeedbackOutput):
        self.pr_info = pr_info
        # self.test_cases = test_cases
        self.feedback_output = feedback_output

    def get_pr_info(self) -> PullRequestInfo:
        return self.pr_info
    
    def get_test_cases(self) -> list[TestCase]:
        return self.test_cases

    def get_feedback_output(self) -> FeedbackOutput:
        return self.feedback_output