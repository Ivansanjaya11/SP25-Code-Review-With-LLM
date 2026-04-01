from Pipeline import Pipeline
from PullRequestMiner import PullRequestMiner
from LLM import LLM
from JSONSaver import JSONSaver
from TestCaseGenerator import TestCaseGenerator
from Output import Output
from pathlib import Path

"""
Pipeline 1:
mines Github repo, get a specific pull request, generate test cases,
get errors and their fix suggestions, save the result
"""
class Pipeline1(Pipeline):
    def __init__(self, repo_url: str, pr_id_list: list[int], model: str):
        super().__init__()
        self.pr_id_list = pr_id_list
        self.pr_miner = PullRequestMiner(repo_url)
        self.test_case_generator = TestCaseGenerator()
        self.llm = LLM(model, prompt_config_path="prompts.json")
       
    def run(self) -> list[Output]:
        self.pr_miner.mine_pr(self.pr_id_list)

        for pr in self.pr_miner.get_pull_request_info_list():
            test_cases = self.test_case_generator.generate(pr)
            feedback = self.llm.execute(pr.get_changes())
            output = Output(pr, test_cases, feedback)
            self.output_list.append(output)
            json_saver = JSONSaver(output)
            json_saver.save()

        return self.output_list