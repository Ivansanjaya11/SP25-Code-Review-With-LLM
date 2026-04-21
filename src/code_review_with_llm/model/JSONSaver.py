import json
import os
from pathlib import Path

from src.code_review_with_llm.output_objects.FeedbackOutput import FeedbackOutput
from src.code_review_with_llm.output_objects.Output import Output

"""
Class that saves to json file
"""
class JSONSaver:
    def __init__(self, output: Output):
        self.output = output
        self.path = None

    def _create_path(self, feedback: FeedbackOutput, pr_id: int, repo_name: str) -> None:
        month = feedback.get_timestamp().month
        year = feedback.get_timestamp().year
        day = feedback.get_timestamp().day
        hour = feedback.get_timestamp().hour
        minute = feedback.get_timestamp().minute

        repo_name = "_".join(repo_name.split(" "))

        directory = (Path("results") / f"{str(year)}_{str(month)}")

        os.makedirs(directory, exist_ok=True)

        filename = f"{year}_{month}_{day}_{hour}_{minute}_{repo_name}_{pr_id}.json"

        self.path = directory / filename

    def save(self) -> None:
        pr_info = self.output.get_pr_info()
        feedback = self.output.get_feedback_output()
        test_cases = self.output.get_test_cases()

        self._create_path(feedback, pr_info.get_id(), pr_info.get_repo_info().get_repo_name())

        data = {
            "pr_info": {
                "pr_id": pr_info.get_id(),
                "pr_title": pr_info.get_title(),
                "pr_description": pr_info.get_description(),
                "pr_changes": pr_info.get_changes(),
                "pr_commit_id_list": pr_info.get_commit_id_list()
            },
            "repository_info": {
                "repo_name": pr_info.get_repo_info().get_repo_name(),
                "repo_url": pr_info.get_repo_info().get_repo_url(),
                "repo_branches": pr_info.get_repo_info().get_branches_names(),
                "repo_commit_id_list": pr_info.get_repo_info().get_commit_id_list(),
                "repo_changes": None
            },
            "test_cases": [
                {
                    "test_filename": test_case.get_test_filename(),
                    "test_filepath": str(test_case.get_test_filepath().resolve()),
                    "test": test_case.get_test()
                } for test_case in test_cases
            ],
            "errors": [
                {
                    "error_type": error.get_error_type(),
                    "severity": error.get_error_severity_level(),
                    "description": error.get_error_description(),
                    "code": error.get_code(),
                    "suggestion": error.get_fix_suggestion()
                }
                for error in feedback.get_all_errors()
            ],
            "timestamp": str(feedback.get_timestamp())
        }

        with open(self.path.resolve(), "w") as file:
            json.dump(data, file, indent=4)
