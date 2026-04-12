from src.code_review_with_llm.Model import Model
from src.code_review_with_llm.View import View
from typing import Any
from src.code_review_with_llm.output_objects.Output import Output

"""
Controller class based on the MVC architecture
"""
class Controller:
    def __init__(self, model: Model = None, view: View = None):
        self.model = model
        self.view = view

    def set_model(self, model: Model) -> None:
        self.model = model

    def set_view(self, view) -> None:
        self.view = view

    def send_to_view1(self, output_list: list[Output]):
        self.view.receive_output_1(output_list)

    def send_to_view2(self, output_list: list[list[Output]]):
        self.view.receive_output_2(output_list)

    def run(self, args: list[Any], pipeline_type: int = 1, is_pdf: bool = True) -> None:
        match pipeline_type:
            case 1: # pipeline 1
                repo_url = args[0]
                pr_id_list = args[1]
                provider = args[2]

                self.model.run_pipeline1(repo_url, pr_id_list, provider, is_pdf)

            case 2: # pipeline 2
                month1 = args[0]
                month2 = args[1]
                year1 = args[2]
                year2 = args[3]

                self.model.run_pipeline2(month1, month2, year1, year2, is_pdf)

            case _:
                print("Unknown pipeline!")