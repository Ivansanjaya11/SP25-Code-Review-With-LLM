from pydriller import Repository
from RepositoryInfo import RepositoryInfo
from PullRequestInfo import PullRequestInfo
from github import Github, Auth
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

class RepoMiner:
    '''
    This class mines a repo and creates PullRequestInfo objects from the mined
    commits.
    '''
    def __init__(self, repo_url: str):
        self.repository = Repository(repo_url)
        self.repo_name = repo_url.split("/")[-1]
        self.repo_owner = repo_url.split("/")[-2]
        self.repository_info = RepositoryInfo(self.repo_name, repo_url, [])
        self.pr_list = []
        self.g = self.set_up_github_api()

    def set_up_github_api(self) -> Github:
        load_dotenv()

        api_key = os.getenv("GITHUB_API_KEY")
        
        if not api_key:
            raise RuntimeError("Missing GITHUB_API_KEY. Set it in your environment or .env file.")
        
        print(f"API Key loaded: {api_key}")

        auth = Auth.Token(api_key)

        g = Github(auth=auth)

        return g
    
    def mine_pr(self, pr_number) -> None:
        full_repo_name = f"{self.repo_owner}/{self.repo_name}"
        repo = self.g.get_repo(full_repo_name)
        
        try: 
            pr = repo.get_pull(pr_number)
            commit_list = pr.get_commits()
            commit_id_list = [commit.sha for commit in commit_list]
        except Exception as e:
            print(f"Error retrieving the pull request: {e}")

        changes = ""

        for commit in pr.get_commits():
            for file in commit.files:
                changes += file.patch
        
        pr_id = pr_number
        pr_title = pr.title
        pr_description = pr.body
        commit_id_list = commit_id_list
        pr_info = PullRequestInfo(pr_id, pr_title, pr_description, 
                                    commit_id_list, changes, 
                                    self.repository_info )
        self.pr_list.append(pr_info)

    def mine_repo(self) -> None:
        
        for idx, commit in enumerate(self.repository.traverse_commits()):
            changes = ""
            for file in commit.modified_files:
                changes += file.diff
            
            pr_id = idx
            pr_title = commit.msg
            pr_description = commit.msg
            commit_id_list = [commit.hash]
            pr_info = PullRequestInfo(pr_id, pr_title, pr_description, 
                                      commit_id_list, changes, 
                                      self.repository_info )
            self.pr_list.append(pr_info)
            

    def get_pull_request_info(self) -> list[PullRequestInfo]:
        return self.pr_list