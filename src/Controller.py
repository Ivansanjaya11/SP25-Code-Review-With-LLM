from Model import Model
from View import View
from typing import Any
from Output import Output

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
        # needs to be changes after making the interface
        print("reached sent to view1!")

    def send_to_view2(self, output_list: list[list[Output]]):
        # needs to be changes after making the interface
        for i in output_list:
            for j in i:
                print(j)
        print("reached sent to view2!")

    def run(self, args: list[Any], pipeline_type: int = 1) -> None:
        match pipeline_type:
            case 1: # pipeline 1
                repo_url = args[0]
                pr_id_list = args[1]
                ollama_model = args[2]

                self.model.run_pipeline1(repo_url, pr_id_list, ollama_model)

            case 2: # pipeline 2
                month1 = args[0]
                month2 = args[1]
                year1 = args[2]
                year2 = args[3]

                self.model.run_pipeline2_range(month1, month2, year1, year2)

            case _:
                print("Unknown pipeline!")