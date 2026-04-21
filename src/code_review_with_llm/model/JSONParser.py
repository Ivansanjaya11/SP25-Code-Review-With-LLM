import json
from datetime import datetime
from pathlib import Path

from src.code_review_with_llm.output_objects.Error import Error
from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput
from src.code_review_with_llm.output_objects.Output import Output
from src.code_review_with_llm.output_objects.PullRequestInfo import PullRequestInfo
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo
from src.code_review_with_llm.output_objects.TestCase import TestCase

"""
Class that parses json file
"""
class JSONParser:
    def __init__(self):
        # list of list of outputs. The outer list represents groupings by month & year
        # inner list represents each feedback saved in that month & year
        self.outputs = []

    # for now, the filter is based on month and year only
    def filter_and_parse(self, month=-1, year=-1) -> list[Output]:
        # parse every json files in results directory recursively
        if month == -1 and year == -1:
            self._parse_everything()

        # parse by a specific year and month
        if month != -1 and year != -1:
            self._parse_by_month_year(month, year)

        return self.outputs

    def _parse_by_month_year(self, month, year) -> None:

        # create the path of the specific month and year director
        a_dir_path = (Path("results") / f"{str(year)}_{str(month)}").resolve()

        # if the directory of that specific month and year doesn't exist, append an empty list
        if not self._check_dir(month, year):
            return

        # iterate through each file in that year_month directory
        # parse the json file
        for file in a_dir_path.iterdir():
            a_file_path = a_dir_path / file
            output = self.parse(a_file_path)
            self.outputs.append(output)

    def _parse_everything(self) -> None:
        # iterate through each year_month directory
        for directory in Path("results").iterdir():
            output_list = []

            year = directory.name.split("_")[0]
            month = directory.name.split("_")[1]

            # create the path of the specific month and year directory
            a_dir_path = (Path("results") / f"{str(year)}_{str(month)}").resolve()

            # iterate through each file in each year_month_directory
            # parse the json file
            for file in a_dir_path.iterdir():
                a_file_path = a_dir_path / file
                output = self.parse(a_file_path)
                output_list.append(output)

            self.outputs.append(output_list)

    def parse(self, path: Path) -> Output:
        # load the json file
        try:
            with open(path.resolve(), 'r', encoding = "utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError as e:
            print(f"Failed to decode json file: {e}")

        # get the dictionary of info of the feedbacks
        pr_info_dict = data["pr_info"]
        repo_info_dict = data["repository_info"]
        test_dict_list = data["test_cases"]
        errors_dict_list = data["errors"]
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")

        # create pr object
        pr_info = self._create_pr(pr_info_dict, repo_info_dict)

        # create feedback object
        feedback = self._create_feedback(errors_dict_list, timestamp)

        # create test case object
        test_cases = self._create_test_cases(test_dict_list)

        # create output object
        output = Output(pr_info, test_cases, feedback)

        return output

    def _create_test_cases(self, test_dict_list) -> list[TestCase]:
        test_cases = []

        for test_case in test_dict_list:
            test_filename = test_case["test_filename"]
            test_filepath = Path(test_case["test_filepath"])
            test = test_case["test"]

            test_case = TestCase(test_filename, test_filepath, test)

            test_cases.append(test_case)

        return test_cases

    def _create_feedback(self, errors_dict_list, timestamp) -> FeedbackOutput:
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


    def _create_pr(self, pr_info_dict, repo_info_dict) -> PullRequestInfo:
        pr_id = pr_info_dict["pr_id"]
        pr_title = pr_info_dict["pr_title"]
        pr_description = pr_info_dict["pr_description"]
        pr_changes = pr_info_dict["pr_changes"]
        pr_commit_id_list = pr_info_dict["pr_commit_id_list"]

        repo_info = self._create_repo(repo_info_dict)

        pull_request_info = PullRequestInfo(pr_id, pr_title, pr_description, pr_commit_id_list, pr_changes, repo_info)

        return pull_request_info

    def _create_repo(self, repo_info_dict) -> RepositoryInfo:
        repo_name = repo_info_dict["repo_name"]
        repo_url = repo_info_dict["repo_url"]
        repo_branches = repo_info_dict["repo_branches"]
        repo_commit_id_list = repo_info_dict["repo_commit_id_list"]
        repo_changes = repo_info_dict["repo_changes"]

        repo_info = RepositoryInfo(repo_name, repo_url, repo_branches, repo_commit_id_list, repo_changes)

        return repo_info

    def _check_dir(self, month, year) -> bool:
        a_dir_path = (Path("results") / f"{str(year)}_{str(month)}").resolve()
        return a_dir_path.is_dir()
