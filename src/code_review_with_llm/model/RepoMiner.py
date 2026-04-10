from pydriller import Repository
from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo
from github import Github, Auth
from dotenv import load_dotenv
import os

class RepoMiner:
    '''
    This class mines a repo and creates a RepoistoryInfo object from the mined
    commits.
    '''
    def __init__(self, repo_url: str):
        self.repository = Repository(repo_url)
        self.repo_name = repo_url.split("/")[-1]
        self.repo_owner = repo_url.split("/")[-2]
        self.repository_info = RepositoryInfo(self.repo_name, repo_url)
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

    def mine_repo(self) -> None:
        full_repo_name = f"{self.repo_owner}/{self.repo_name}"
        repo = self.g.get_repo(full_repo_name)

        repo_description = repo.description
        repo_branches_names = [branch.name for branch in repo.get_branches()]
        commit_id_list = []

        for _, commit in enumerate(self.repository.traverse_commits()):
            changes = ""
            for file in commit.modified_files:
                for _, line in file.diff_parsed["added"]:
                    changes += line + "\n"

            commit_id_list.append(commit.hash)

        self.repository_info.set_commit_id_list(commit_id_list)
        self.repository_info.set_repo_description(repo_description)
        self.repository_info.set_branches_names(repo_branches_names)

    def get_repository_info(self) -> RepositoryInfo:
        return self.repository_info