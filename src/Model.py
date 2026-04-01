from Pipeline1 import Pipeline1
from Pipeline2 import Pipeline2
from pathlib import Path
from Output import Output

"""
Model class based on the MVC architecture.
"""
class Model:
    def __init__(self, controller):
        self.controller = controller

    def run_pipeline1(self, repo_url: str, pr_id_list: list[int], model: str) -> None:
        pipeline1 = Pipeline1(repo_url, pr_id_list, model)
        output_list = pipeline1.run()
        self.send_to_controller(output_list)

    def run_pipeline2(self, path: Path) -> None:
        pipeline2 = Pipeline2(path)
        output_list = pipeline2.run()
        self.send_to_controller(output_list)

    def send_to_controller(self, output_list: list[Output]) -> None:
        self.controller.send_to_view(output_list)
