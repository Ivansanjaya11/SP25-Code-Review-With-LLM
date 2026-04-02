from Pipeline1 import Pipeline1
from Pipeline2 import Pipeline2
from Output import Output

"""
Model class based on the MVC architecture.
"""
class Model:
    def __init__(self, controller: "Controller"):
        self.controller = controller

    def run_pipeline1(self, repo_url: str, pr_id_list: list[int], model: str) -> None:
        pipeline1 = Pipeline1(repo_url, pr_id_list, model)
        output_list = pipeline1.run()
        self.send_to_controller_1(output_list)

    def _run_pipeline2(self, month: int, year: int) -> list[list[Output]]:
        # pipeline 2 when the user searches for saved feedbacks in a specific month & year

        pipeline2 = Pipeline2(month, year)
        output_list = pipeline2.run()

        return output_list

    def run_pipeline2_range(self, month1: int, month2: int, year1: int, year2:int) -> list[list[Output]]:
        # pipeline 2 when the user searches for saved feedbacks in a range of months and year

        outputs_list = []

        for year in range(year1, year2+1):
            for month in range(month1, month2+1):
                output_list = self._run_pipeline2(month, year)
                an_output_list = output_list[0]
                outputs_list.append(an_output_list)

        return outputs_list

    def send_to_controller_1(self, output_list: list[Output]) -> None:
        self.controller.send_to_view1(output_list)

    def send_to_controller_2(self, output_list: list[list[Output]]) -> None:
        self.controller.send_to_view2(output_list)
