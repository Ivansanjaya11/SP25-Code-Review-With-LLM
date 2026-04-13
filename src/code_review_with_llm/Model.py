from src.code_review_with_llm.model.Pipeline1 import Pipeline1
from src.code_review_with_llm.model.Pipeline2 import Pipeline2
from src.code_review_with_llm.model.Pipeline3 import Pipeline3
from src.code_review_with_llm.output_objects.Output import Output
from src.code_review_with_llm.model.GeminiLLM import GeminiLLM
from src.code_review_with_llm.model.OllamaLLM import OllamaLLM

"""
Model class based on the MVC architecture.
"""
class Model:
    def __init__(self, controller: "Controller"):
        self.controller = controller

    def run_pipeline1(self, repo_url: str, pr_id_list: list[int], provider: str = "gemini", is_pdf: bool = True) -> None:
        if provider == "gemini":
            llm = GeminiLLM()
        else:
            llm = OllamaLLM()

        pipeline1 = Pipeline1(repo_url, pr_id_list, llm, is_pdf)
        output_list = pipeline1.run()
        self.send_to_controller_1(output_list)

    def run_pipeline2(self, month1: int, month2: int, year1: int, year2:int, is_pdf: bool = True) -> None:
        pipeline2 = Pipeline2(month1, month2, year1, year2, is_pdf)
        outputs_list = pipeline2.run()
        self.send_to_controller_2(outputs_list)

    def run_pipeline3(self, repo_url: str, provider: str = "gemini") -> None:
        if provider == "gemini":
            llm = GeminiLLM()
        else:
            llm = OllamaLLM()

        pipeline3 = Pipeline3(repo_url, llm)

        analysis: str = pipeline3.run()

        self.send_to_controller_3(analysis)

    def send_to_controller_1(self, output_list: list[Output]) -> None:
        self.controller.send_to_view1(output_list)

    def send_to_controller_2(self, output_list: list[list[Output]]) -> None:
        self.controller.send_to_view2(output_list)

    def send_to_controller_3(self, analysis: str) -> None:
        self.controller.send_to_view3(analysis)