from Output import Output
import json

class JSONSaver:
    def __init__(self, output: Output, path: str = "results/output.json"):
        self.output = output
        self.path = path

    def save(self):
        pr_info = self.output.get_pr_info()
        feedback = self.output.get_feedback_output()
    
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
                "repo_commit_id_list": pr_info.get_repo_info().get_commit_id_list()
            },
            "errors": [
                {
                    "error_type": error.get_error_type(),
                    "severity": error.get_error_severity_level(),
                    "description": error.get_error_description(),
                    "suggestion": error.get_fix_suggestion()
                }
                for error in feedback.get_all_errors()
            ],
            "timestamp": str(feedback.get_timestamp())
        }

        with open(self.path, "w") as file:
            json.dump(data, file, indent=4)
