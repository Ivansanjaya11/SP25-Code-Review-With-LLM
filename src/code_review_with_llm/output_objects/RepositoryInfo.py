from src.code_review_with_llm.output_objects.Analysis import Analysis

class RepositoryInfo:
    '''
    Object that holds the details of a repository to be used by PullRequestInfo'''
    def __init__(self, repo_name: str, repo_url: str, repo_owner: str,
                 branches_names: list[str] = [], commit_id_list: list[str] = None,
                 analysis_list: list[Analysis] = None):
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.repo_owner = repo_owner
        self.branches_names = branches_names
        self.repo_details = ""
        self.commit_id_list = commit_id_list
        self.analysis_list = analysis_list

    def get_repo_details(self) -> str:
        return self.repo_details
    
    def get_repo_name(self) -> str:
        return self.repo_name

    def get_repo_owner(self) -> str:
        return self.repo_owner
    
    def get_branches_names(self) -> list[str]:
        return self.branches_names
    
    def get_repo_url(self) -> str:
        return self.repo_url

    def get_commit_id_list(self) -> list[str]:
        return self.commit_id_list

    def get_analysis_list(self) -> list[Analysis]:
        return self.analysis_list

    def set_branches_names(self, branches_names) -> None:
        self.branches_names = branches_names

    def set_repo_description(self, repo_description) -> None:
        self.repo_details = repo_description

    def set_commit_id_list(self, commit_id_list) -> None:
        self.commit_id_list = commit_id_list

    def set_analysis_list(self, analysis_list: list[Analysis]) -> None:
        self.analysis_list = analysis_list