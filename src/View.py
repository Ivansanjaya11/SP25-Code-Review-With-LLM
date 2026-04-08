from typing import Any
from textual.app import App, ComposeResult
from textual import on
from textual.widgets import Label, Button, Input, RadioButton, RadioSet, Header
from textual.validation import Number
from datetime import date

"""
View class based on the MVC architecture
"""
class View(App[str]):
    def __init__(self, controller: "Controller"):
        super().__init__()
        self.theme = "tokyo-night"
        self.title = "CODE REVIEW WITH LLM"
        self.controller = controller

    def receive_output_1(self, output_list):
        pass

    def receive_output_2(self, outputs_list):
        pass

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield Input(placeholder="Enter repository url: ", id="repo_url")
        yield Input(
            placeholder="Enter pull request ID: ",
            restrict=r"\d*",
            id="pr_id"
        )
        yield Label("Do you want a PDF report?")
        with RadioSet(id="is_pdf_review"):
            yield RadioButton("Yes", id="yes", value=False)
            yield RadioButton("No", id="no", value=False)

        yield Button("Review pull Request", id="review_pr", variant="primary")

        yield Input(
            placeholder="From month (1-12): ",
            restrict=r"[0-9]*",
            max_length=2,
            validators=[Number(minimum=1, maximum=12)],
            id="from_month"
        )
        yield Input(
            placeholder="Until month (1-12): ",
            restrict=r"[0-9]*",
            max_length=2,
            validators=[Number(minimum=1, maximum=12)],
            id="until_month"
        )
        yield Input(
            placeholder="From Year (4 digit): ",
            restrict=r"[0-9]*",
            max_length=4,
            validators=[Number(minimum=1900, maximum=date.today().year)],
            id="from_year"
        )
        yield Input(
            placeholder="Until Year (4 digit): ",
            restrict=r"[0-9]*",
            max_length=4,
            validators=[Number(minimum=1900, maximum=date.today().year)],
            id="until_year"
        )
        yield Label("Do you want a PDF report?")
        with RadioSet(id="is_pdf_feedback"):
            yield RadioButton("Yes", id="yes", value=False)
            yield RadioButton("No", id="no", value=False)

        yield Button("Display saved feedback", id="display_feedback", variant="primary")

        yield Button("Exit", id="exit_button", variant="error")

    @on(Button.Pressed, "#exit_button")
    def handle_exit(self):
        self.exit()

    @on(Button.Pressed, "#review_pr")
    def handle_pr_review(self):
        repo_url = str(self.query_one("#repo_url", Input).value)
        pr_id = [int(self.query_one("#pr_id", Input).value)]

        is_pdf_radio = self.query_one("#is_pdf_review", RadioSet)
        selected = str(is_pdf_radio.pressed_button)

        is_pdf = False

        if selected:
            if selected == "Yes":
                is_pdf = True

        ollama_model = "llama3:latest"

        self.execute([repo_url, pr_id, ollama_model], 1, is_pdf)

    @on(Button.Pressed, "#display_feedback")
    def handle_display_feedback(self):
        from_month = int(self.query_one("#from_month", Input).value)
        until_month = int(self.query_one("#until_month", Input).value)
        from_year = int(self.query_one("#from_year", Input).value)
        until_year = int(self.query_one("#until_year", Input).value)

        is_pdf_radio = self.query_one("#is_pdf_feedback", RadioSet)
        selected = str(is_pdf_radio.pressed_button)

        is_pdf = False

        if selected:
            if selected == "Yes":
                is_pdf = True

        self.execute([from_month, until_month, from_year, until_year], 2, is_pdf)

    async def on_mount(self) -> None:
        pass

    def execute(self, args: list[Any], pipeline_type: int = 1, is_pdf: bool = True) -> None:
        #ollama_model = "llama3:latest"

        # repo_url = "https://github.com/Ivansanjaya11/SP25-Code-Review-With-LLM"
        #repo_url = "https://github.com/psf/requests"
        #pr_id_list = [7315]

        #args = [repo_url, pr_id_list, ollama_model]
        #pipeline_type = 1
        #is_pdf = True

        self.controller.run(args, pipeline_type, is_pdf)
        # controller.run([4, 5, 2026, 2026], 2)
        # controller.run([-1, -1, -1, -1], 2)

