from src.code_review_with_llm.output_objects.RepositoryInfo import RepositoryInfo
from github import PullRequest

class PullRequestInfo:
    '''
    This class contains all of the information on a pull request mined with 
    RepoMiner.
    '''
    def __init__(self, pr_id: int, pr_title: str, pr_description: str, 
                 commit_id_list: list[str], changes: str, 
                 repository_info: RepositoryInfo, pull_request: PullRequest = None):
        self.pr_id = pr_id
        self.pr_title = pr_title
        self.pr_description = pr_description
        self.commit_id_list = commit_id_list
        self.changes = changes
        self.repository_info = repository_info
        self.pull_request = pull_request

    def get_pr_details(self) -> None:
        string = ""

        string += "From repository: " + self.repository_info.get_repo_name() + "\n"
        string += "pull request id: " + str(self.pr_id) + "\n"
        string += "title: " + self.pr_title + "\n"
        string += "description:\n" + self.pr_description

        print(string)

    def get_changes(self) -> str:
        return self.changes
    
    def get_id(self) -> int:
        return self.pr_id
    
    def get_description(self) -> str:
        return self.pr_description
    
    def get_title(self) -> str:
        return self.pr_title
    
    def get_pull_request(self) -> PullRequest:
        return self.pull_request
    
    def get_commit_id_list(self) -> list[str]:
        return self.commit_id_list
    
    def get_repo_info(self) -> RepositoryInfo:
        return self.repository_info
        