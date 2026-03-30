from Pipeline import Pipeline
from PullRequestMiner import PullRequestMiner
from LLM import LLM
from Output import Output

class Pipeline1(Pipeline):
    def __init__(self, repo_url: str, pr_id_list: list[int], model: str):
        super().__init__()
        self.pr_id_list = pr_id_list
        self.pr_miner = PullRequestMiner(repo_url)
        self.llm = LLM(model, prompt_config_path="prompts.json")
       
    def run(self):
        self.pr_miner.mine_pr(self.pr_id_list)

        for pr in self.pr_miner.get_pull_request_info_list():
            feedback = self.llm.execute(pr.get_changes())
            output = Output(pr, feedback)
            self.output.append(output)
