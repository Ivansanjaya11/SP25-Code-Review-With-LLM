from pydriller import Repository
from RepositoryInfo import RepositoryInfo
from PullRequestInfo import PullRequestInfo

class RepoMiner:
    '''
    This class mines a repo and creates PullRequestInfo objects from the mined
    commits.
    '''
    def __init__(self, repo_url: str):
        self.repository = Repository(repo_url)
        repo_name = repo_url.split("/")[-1]
        self.repository_info = RepositoryInfo(repo_name, repo_url, [])
        self.pr_list = []

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