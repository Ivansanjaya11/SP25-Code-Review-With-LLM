from Output import Output
from pathlib import Path
import json
from FeedbackOutput import FeedbackOutput
from PullRequestInfo import PullRequestInfo
from RepositoryInfo import RepositoryInfo
from TestCase import TestCase
from Error import Error

"""
Class that parses json file
"""
class JSONParser:
    def __init__(self, path: Path):
        self.path = path

    def set_path(self, path: Path) -> None:
        self.path = path

    def parse(self) -> Output:
        try:
            with open(self.path.resolve(), 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Failed to decode json file")

        pr_info_dict = data["pr_info"]
        repo_info_dict = data["repository_info"]
        test_dict_list = data["test_cases"]
        errors_dict_list = data["errors"]
        timestamp = data["timestamp"]

        pr_info = self.create_pr(pr_info_dict, repo_info_dict)

        feedback = self.create_feedback(errors_dict_list, timestamp)

        test_cases = self.create_test_cases(test_dict_list)

        output = Output(pr_info, test_cases, feedback)

        return output

    def create_test_cases(self, test_dict_list) -> list[TestCase]:
        test_cases = []

        for test_case in test_dict_list:
            test_filename = test_case["test_filename"]
            test_filepath = Path(test_case["test_filepath"])
            test = test_case["test"]

            test_case = TestCase(test_filename, test_filepath, test)

            test_cases.append(test_case)

        return test_cases

    def create_feedback(self, errors_dict_list, timestamp) -> FeedbackOutput:
        feedback = FeedbackOutput([], timestamp)

        for an_error_info in errors_dict_list:
            error_type = an_error_info["error_type"]
            severity = an_error_info["severity"]
            description = an_error_info["description"]
            code = an_error_info["code"]
            suggestion = an_error_info["suggestion"]

            error = Error(error_type, severity, description, code, suggestion)

            feedback.add_error(error)

        return feedback


    def create_pr(self, pr_info_dict, repo_info_dict) -> PullRequestInfo:
        pr_id = pr_info_dict["pr_id"]
        pr_title = pr_info_dict["pr_title"]
        pr_description = pr_info_dict["pr_description"]
        pr_changes = pr_info_dict["pr_changes"]
        pr_commit_id_list = pr_info_dict["pr_commit_id_list"]

        repo_info = self.create_repo(repo_info_dict)

        pull_request_info = PullRequestInfo(pr_id, pr_title, pr_description, pr_commit_id_list, pr_changes, repo_info)

        return pull_request_info

    def create_repo(self, repo_info_dict):
        repo_name = repo_info_dict["repo_name"]
        repo_url = repo_info_dict["repo_url"]
        repo_branches = repo_info_dict["repo_branches"]
        repo_commit_id_list = repo_info_dict["repo_commit_id_list"]
        repo_changes = repo_info_dict["repo_changes"]

        repo_info = RepositoryInfo(repo_name, repo_url, repo_branches, repo_commit_id_list, repo_changes)

        return repo_info