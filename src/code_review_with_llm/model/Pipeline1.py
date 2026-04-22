from src.code_review_with_llm.model.JSONSaver import JSONSaver
from src.code_review_with_llm.model.LLM import LLM
from src.code_review_with_llm.model.PDFGenerator import PDFGenerator
from src.code_review_with_llm.model.Pipeline import Pipeline
from src.code_review_with_llm.model.PullRequestMiner import PullRequestMiner
from src.code_review_with_llm.model.TestCaseGenerator import TestCaseGenerator
from src.code_review_with_llm.output_objects.Output import Output

"""
Pipeline 1:
mines Github repo, get a specific pull request, generate test cases,
get errors and their fix suggestions, save the result
"""
class Pipeline1(Pipeline):
    def __init__(self, repo_url: str, pr_id_list: list[int], llm: LLM, is_pdf: bool = True):
        super().__init__()
        self.pr_id_list = pr_id_list
        self.pr_miner = PullRequestMiner(repo_url)
        self.test_case_generator = TestCaseGenerator()
        self.llm = llm
        self.is_pdf = is_pdf

    def run(self) -> list[Output]:
        # step 1: mine Github repository
        self.pr_miner.mine_pr(self.pr_id_list)

        for pr in self.pr_miner.get_pull_request_info_list():
            # step 2: generate test cases
            try:
                test_cases = self.test_case_generator.generate(pr)
            except Exception as e:
                print(f"Test case generation failed: {e}")
                test_cases = []

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
                self._generate_pdf(output)

        return self.output_list

    def _generate_pdf(self, output: Output) -> None:
            pdf = PDFGenerator(output)
            pdf.generate()
            print('PDF Generated!')
