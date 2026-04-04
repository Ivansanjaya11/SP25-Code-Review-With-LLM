from Pipeline import Pipeline
from PullRequestMiner import PullRequestMiner
from LLM import LLM
from JSONSaver import JSONSaver
from TestCaseGenerator import TestCaseGenerator
from Output import Output
from PDFGenerator import PDFGenerator

"""
Pipeline 1:
mines Github repo, get a specific pull request, generate test cases,
get errors and their fix suggestions, save the result
"""
class Pipeline1(Pipeline):
    def __init__(self, repo_url: str, pr_id_list: list[int], model: str, is_pdf: bool = True):
        super().__init__()
        self.pr_id_list = pr_id_list
        self.pr_miner = PullRequestMiner(repo_url)
        self.test_case_generator = TestCaseGenerator()
        self.llm = LLM(model, prompt_config_path="prompts.json")
        self.is_pdf = is_pdf
       
    def run(self) -> list[Output]:
        # step 1: mine Github repository
        self.pr_miner.mine_pr(self.pr_id_list)

        for pr in self.pr_miner.get_pull_request_info_list():
            # step 2: generate test cases
            test_cases = self.test_case_generator.generate(pr)

            # step 3: get errors and their suggestions
            feedback = self.llm.execute(pr.get_changes())

            # step 4: create an Output object
            output = Output(pr, test_cases, feedback)
            self.output_list.append(output)

            # step 5: save to json file
            json_saver = JSONSaver(output)
            json_saver.save()

            # step 6: generate pdf (optional)
            if self.is_pdf:
                self.generate_pdf(output)

        return self.output_list

    def generate_pdf(self, output: Output) -> None:
            pdf = PDFGenerator(output)
            pdf.generate()
            print('PDF Generated!')