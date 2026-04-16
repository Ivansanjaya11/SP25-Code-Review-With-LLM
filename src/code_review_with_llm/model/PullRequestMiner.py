from pydriller import Repository
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo
from src.code_review_with_llm.output_objects.PullRequestInfo import PullRequestInfo
from github import Github, Auth
from dotenv import load_dotenv
import os

class PullRequestMiner:
    '''
    This class mines a specific pull request in a GitHub repository and creates PullRequestInfo objects from the mined
    commits.
    '''

    def __init__(self, repo_url: str):
        self.repo_name = repo_url.split("/")[-1]
        self.repo_owner = repo_url.split("/")[-2]
        self.repo_url = repo_url
        self.repository_info = RepositoryInfo(self.repo_name, repo_url, [])
        self.pr_list = []
        self.g = self.set_up_github_api()

    def set_up_github_api(self) -> Github:
        load_dotenv()

        api_key = os.getenv("GITHUB_API_KEY")

        if not api_key:
            raise RuntimeError("Missing GITHUB_API_KEY. Set it in your environment or .env file.")

        print("API Key loaded")

        auth = Auth.Token(api_key)

        g = Github(auth=auth)

        return g

    def mine_pr(self, pr_id_list: list[int]) -> None:
        full_repo_name = f"{self.repo_owner}/{self.repo_name}"
        repo = self.g.get_repo(full_repo_name)

        for pr_id in pr_id_list:
            try:
                pr = repo.get_pull(pr_id)
                commit_list = pr.get_commits()
                commit_id_list = [commit.sha for commit in commit_list]

                changes = ""

                for commit in pr.get_commits():
                    for file in commit.files:
                        for line in file.patch.splitlines():
                            if line.startswith('+') and not line.startswith('+++'):
                                changes += line[1:] + "\n"

                pr_title = pr.title
                pr_description = pr.body
                pr_info = PullRequestInfo(pr_id, pr_title, pr_description,
                                        commit_id_list, changes,
                                        self.repository_info, pr)
                self.pr_list.append(pr_info)
            except Exception as e:
                print(f"Error retrieving the pull request for {self.repo_url}: {e}")
                continue

    def get_pull_request_info_list(self) -> list[PullRequestInfo]:
        return self.pr_list