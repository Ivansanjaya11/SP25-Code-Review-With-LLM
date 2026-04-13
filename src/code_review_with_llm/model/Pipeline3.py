from src.code_review_with_llm.model.LLM import LLM
from src.code_review_with_llm.model.Pipeline import Pipeline
from src.code_review_with_llm.model.RepoMiner import RepoMiner

class Pipeline3(Pipeline):
    def __init__(self, repo_url: str, llm: LLM):
        super().__init__()
        self.repo_url = repo_url
        self.repo_miner = RepoMiner(self.repo_url)
        self.llm = llm

    def run(self) -> str:
        # step 1: mine Github repository
        self.repo_miner.mine_repo()

        repo_info = self.repo_miner.get_repository_info()

        changes = repo_info.get_changes()

        analysis = self.llm.request_repo_analysis(changes)

        print("analysis passed back to view!")

        return analysis