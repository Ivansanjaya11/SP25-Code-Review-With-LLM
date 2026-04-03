from Output import Output
import os
from pathlib import Path
from FeedbackOutput import FeedbackOutput
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class PDFGenerator:
    def __init__(self, output: Output):
        self.output = output
        self.path = None
        self.filename = None

    def create_path(self, feedback: FeedbackOutput, pr_id: int, repo_name: str) -> None:
        month = feedback.get_timestamp().month
        year = feedback.get_timestamp().year
        day = feedback.get_timestamp().day
        hour = feedback.get_timestamp().hour
        minute = feedback.get_timestamp().minute

        repo_name = "_".join(repo_name.split(" "))

        directory = Path("../generated_pdf") / f"{year}_{month}"

        os.makedirs(directory, exist_ok=True)

        filename = f"{year}_{month}_{day}_{hour}_{minute}_{repo_name}_{pr_id}.pdf"

        self.path = directory / filename

    def generate(self) -> None:
        pr_info = self.output.get_pr_info()
        feedback = self.output.get_feedback_output()
        test_cases = self.output.get_test_cases()

        self.create_path(feedback, pr_info.get_id(), pr_info.get_repo_info().get_repo_name())

        doc = SimpleDocTemplate(str(self.path), pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph(f"{pr_info.get_title()}", styles['Title']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(str(feedback.get_timestamp()), styles['Normal']))

        elements.append(Paragraph("Pull Request", styles['Heading2']))
        elements.append(Paragraph(f"<b>Repository:</b> {pr_info.get_repo_info().get_repo_name()} {pr_info.get_repo_info().get_repo_url()}", styles['Normal']))
        elements.append(Paragraph(f"<b>Title:</b> {pr_info.get_title()}", styles['Normal']))
        elements.append(Paragraph(f"<b>Description:</b> {pr_info.get_description()}", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Errors Found", styles['Heading2']))
        for error in feedback.get_all_errors():
            elements.append(Paragraph(f"<b>Error Type:</b> {error.get_error_type()}", styles['Normal']))
            elements.append(Paragraph(f"<b>Severity:</b> {error.get_error_severity_level()}", styles['Normal']))
            elements.append(Paragraph(f"<b>Description:</b> {error.get_error_description()}", styles['Normal']))
            elements.append(Paragraph(f"<b>Suggestion:</b> {error.get_fix_suggestion()}", styles['Normal'])) 
            elements.append(Spacer(1, 12))

        doc.build(elements)