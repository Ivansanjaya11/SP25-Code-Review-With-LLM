from Pipeline import Pipeline
from pathlib import Path
from JSONParser import JSONParser
from Output import Output

"""
Pipeline 2:
Given a path to a json file,
Parse it and get all the information about previously saved result from pipeline 1
"""
class Pipeline2(Pipeline):
    def __init__(self, path: Path):
        super().__init__()
        self.path = path

    def run(self) -> list[Output]:
        json_parser = JSONParser(self.path)

        output = json_parser.parse()

        self.output_list.append(output)

        return self.output_list
