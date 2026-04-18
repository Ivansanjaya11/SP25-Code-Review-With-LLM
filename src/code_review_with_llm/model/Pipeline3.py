from tqdm import tqdm

from src.code_review_with_llm.model.LLM import LLM
from src.code_review_with_llm.model.Pipeline import Pipeline
from src.code_review_with_llm.model.RepoMiner import RepoMiner
from src.code_review_with_llm.output_objects.Analysis import Analysis


class Pipeline3(Pipeline):
    def __init__(self, repo_url: str, llm: LLM):
        super().__init__()
        self.repo_url = repo_url
        self.repo_miner = RepoMiner(self.repo_url)
        self.llm = llm

    def run(self) -> list[Analysis]:
        # step 1: mine Github repository
        self.repo_miner.mine_repo()

        repo_info = self.repo_miner.get_repository_info()

        analysis_list = repo_info.get_analysis_list()

        print("Requesting repo analysis.....")

        for an_analysis in tqdm(analysis_list, desc="analyzing repo"):
        #for an_analysis in analysis_list:
            changes = an_analysis.get_changes()
            analysis = self.llm.request_repo_analysis(changes)
            an_analysis.set_analysis(analysis)

        print("Repository successfully analyzed!")

        return analysis_list
