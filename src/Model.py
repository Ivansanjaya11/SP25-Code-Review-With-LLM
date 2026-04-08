from Pipeline1 import Pipeline1
from Pipeline2 import Pipeline2
from Output import Output

"""
Model class based on the MVC architecture.
"""
class Model:
    def __init__(self, controller: "Controller"):
        self.controller = controller

    def run_pipeline1(self, repo_url: str, pr_id_list: list[int], model: str, is_pdf: bool = True) -> None:
        pipeline1 = Pipeline1(repo_url, pr_id_list, model, is_pdf)
        output_list = pipeline1.run()
        self.send_to_controller_1(output_list)

    def run_pipeline2(self, month1: int, month2: int, year1: int, year2:int, is_pdf: bool = True) -> None:
        pipeline2 = Pipeline2(month1, month2, year1, year2, is_pdf)
        outputs_list = pipeline2.run()
        self.send_to_controller_2(outputs_list)

    def send_to_controller_1(self, output_list: list[Output]) -> None:
        self.controller.send_to_view1(output_list)

    def send_to_controller_2(self, output_list: list[list[Output]]) -> None:
        self.controller.send_to_view2(output_list)
