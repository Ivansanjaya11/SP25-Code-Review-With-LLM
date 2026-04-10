from src.code_review_with_llm.output_objects.PullRequestInfo import PullRequestInfo
from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput
from src.code_review_with_llm.output_objects.TestCase import TestCase

class Output:
    def __init__(self, pr_info: PullRequestInfo = None,
                 test_cases: list[TestCase] = None,
                 feedback_output: FeedbackOutput = None):
        self.pr_info = pr_info
        self.test_cases = test_cases
        self.feedback_output = feedback_output

    def get_pr_info(self) -> PullRequestInfo:
        return self.pr_info
    
    def get_test_cases(self) -> list[TestCase]:
        return self.test_cases

    def get_feedback_output(self) -> FeedbackOutput:
        return self.feedback_output

    def __str__(self) -> str:
        string = ""

        pr_id = self.pr_info.get_id()
        pr_description = self.pr_info.get_description()
        pr_title = self.pr_info.get_title()

        test_cases = [test_case.get_test_filename() for test_case in self.test_cases]

        timestamp = self.feedback_output.get_timestamp()

        string += "PR ID: " + str(pr_id) + "\n\n"
        string += "Title: " + pr_title + "\n\n"
        string += "Description:\n" + pr_description + "\n\n"

        string += "Test cases names:\n" + str(test_cases) + "\n\n"

        string += "Timestamp: " + str(timestamp) + "\n\n"

        return string