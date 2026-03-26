class RepositoryInfo:
    '''
    Object that holds the details of a repository to be used by PullRequestInfo'''
    def __init__(self, repo_name: str, repo_url: str, branches_names: list[str]):
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.branches_names = branches_names
        self.repo_details = ""

    def get_repo_details(self) -> str:
        return self.repo_details
    
    def get_repo_name(self) -> str:
        return self.repo_name
    
    def get_branches_names(self) -> list[str]:
        return self.branches_names
    
    def get_repo_url(self) -> str:
        return self.repo_url