from typing import Any

"""
View class based on the MVC architecture
"""
class View:
    def __init__(self, controller: "Controller"):
        self.controller = controller

    def run(self, args: list[Any], pipeline_type: int = 1) -> None:
        self.controller.run(args, pipeline_type)

