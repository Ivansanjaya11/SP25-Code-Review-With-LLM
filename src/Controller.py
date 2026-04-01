from Model import Model
from typing import Any
from pathlib import Path
from Output import Output

"""
Controller class based on the MVC architecture
"""
class Controller:
    def __init__(self, model: Model, view):
        self.model = model
        self.view = view

    def set_model(self, model: Model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def send_to_view(self, output_list: list[Output]):
        pass

    def run(self, args: list[Any], pipeline_type: int = 1):
        match pipeline_type:
            case 1: # pipeline 1
                repo_url = args[0]
                pr_id_list = args[1]
                ollama_model = args[3]

                self.model.run_pipeline1(repo_url, pr_id_list, ollama_model)
            case 2: # pipeline 2
                path = Path(args[0])

                self.model.run_pipeline2(path)
            case _:
                print("Unknown pipeline!")
