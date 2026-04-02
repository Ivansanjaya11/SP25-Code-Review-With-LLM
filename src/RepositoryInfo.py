class RepositoryInfo:
    '''
    Object that holds the details of a repository to be used by PullRequestInfo'''
    def __init__(self, repo_name: str, repo_url: str,
                 branches_names: list[str] = [], commit_id_list: list[str] = None,
                 changes: list[str] = None):
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.branches_names = branches_names
        self.repo_details = ""
        self.commit_id_list = commit_id_list
        self.changes = changes

    def get_repo_details(self) -> str:
        return self.repo_details
    
    def get_repo_name(self) -> str:
        return self.repo_name
    
    def get_branches_names(self) -> list[str]:
        return self.branches_names
    
    def get_repo_url(self) -> str:
        return self.repo_url

    def get_commit_id_list(self) -> list[str]:
        return self.commit_id_list

    def get_changes(self) -> list[str]:
        return self.changes

    def set_branches_names(self, branches_names) -> None:
        self.branches_names = branches_names

    def set_repo_description(self, repo_description) -> None:
        self.repo_details = repo_description

    def set_commit_id_list(self, commit_id_list) -> None:
        self.commit_id_list = commit_id_list

    def set_changes(self, changes: str) -> None:
        self.changes = changes