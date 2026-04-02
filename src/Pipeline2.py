from Pipeline import Pipeline
from JSONParser import JSONParser
from Output import Output

"""
Pipeline 2:
Given a path to a json file,
Parse it and get all the information about previously saved result from pipeline 1
"""
class Pipeline2(Pipeline):
    def __init__(self, month: int, year: int):
        super().__init__()
        self.month = month
        self.year = year

    def run(self) -> list[list[Output]]:
        json_parser = JSONParser()
        output = json_parser.filter_and_parse(month=self.month, year=self.year)
        self.output_list = output

        return self.output_list

    # create a PDFGenerator object
    # run the method that generates pdf and stores it
    # prints a confirmation message
    def generate_pdf(self) -> None:
        # use timestamp and other information to dynamically create filename
        # create a folder "generated_pdf"
        # generated pdf automatically put there
        # <ADD HERE>
        pass