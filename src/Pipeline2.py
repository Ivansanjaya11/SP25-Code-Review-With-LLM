from Pipeline import Pipeline
from JSONParser import JSONParser
from Output import Output
from src.PDFGenerator import PDFGenerator

"""
Pipeline 2:
Given a path to a json file,
Parse it and get all the information about previously saved result from pipeline 1
"""
class Pipeline2(Pipeline):
    def __init__(self, month1: int, month2: int, year1: int, year2: int, is_pdf: bool = True):
        super().__init__()
        self.month1 = month1
        self.month2 = month2
        self.year1 = year1
        self.year2 = year2
        self.is_pdf = is_pdf

    def parse(self, month: int, year: int) -> list[Output]:
        json_parser = JSONParser()
        self.output_list = json_parser.filter_and_parse(month=month, year=year)

        if self.is_pdf:
            self.generate_pdf(self.output_list)

        return self.output_list

    def run(self) -> list[list[Output]]:
        outputs_list = []

        for year in range(self.year1, self.year2 + 1):
            for month in range(self.month1, self.month2 + 1):
                output_list = self.parse(month, year)
                outputs_list.append(output_list)

        return outputs_list

    def generate_pdf(self, output_list: list[Output]) -> None:
        for out in output_list:
            pdf = PDFGenerator(out)
            pdf.generate()
            print("PDF generated!")