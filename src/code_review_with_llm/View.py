import customtkinter as ctk
import threading
import json
from src.code_review_with_llm.output_objects.Analysis import Analysis

"""
View class based on the MVC architecture.
CustomTkinter GUI replacement for Textual terminal UI.
"""

# ── Color palette ────────────────────────────────────────────
BG_DARK = "#1a1b26"       # tokyo-night inspired background
BG_CARD = "#24283b"       # card / panel background
ACCENT = "#7aa2f7"        # primary accent blue
ACCENT_HOVER = "#89b4fa"  # hover state
TEXT_PRIMARY = "#c0caf5"   # main text
TEXT_DIM = "#565f89"       # muted text
BORDER = "#414868"         # subtle borders
SUCCESS = "#9ece6a"        # green for positive actions
DANGER = "#f7768e"         # red for exit / errors
WARNING = "#e0af68"        # orange for severity warnings


class View(ctk.CTk):
    def __init__(self, controller: "Controller"):
        super().__init__()
        self.controller = controller

        # ── Window config ────────────────────────────────────
        self.title("Code Review With LLM")
        self.geometry("780x720")
        self.minsize(680, 620)
        self.configure(fg_color=BG_DARK)

        # ── Title frame ───────────────────────────────────────
        title_frame = ctk.CTkFrame(self, fg_color=BG_DARK)
        title_frame.pack(fill="x", padx=30, pady=(24, 0))

        ctk.CTkLabel(
            title_frame,
            text="Code Review With LLM",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Analyze pull requests and view saved feedback",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_DIM,
        ).pack(anchor="w", pady=(2, 0))

        # ── Tab view ────────────────────────────────────────
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=BG_CARD,
            segmented_button_fg_color=BG_DARK,
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color=ACCENT_HOVER,
            segmented_button_unselected_color=BG_CARD,
            segmented_button_unselected_hover_color=BORDER,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
        )
        self.tabview.pack(fill="both", expand=True, padx=30, pady=(16, 8))

        self.tab_review = self.tabview.add("  Review PR  ")
        self.tab_feedback = self.tabview.add("  Saved Feedback  ")
        self.tab_analyze = self.tabview.add("  Analyze Repo  ")

        self._build_review_tab()
        self._build_feedback_tab()
        self._build_analyze_tab()

        # ── Status bar ──────────────────────────────────────
        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_DIM,
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=34, pady=(0, 16))

    # ─────────────────────────────────────────────────────────
    #  Tab 1 – Review Pull Request
    # ─────────────────────────────────────────────────────────
    def _build_review_tab(self):
        tab = self.tab_review
        tab.configure(fg_color=BG_CARD)

        # Repo URL
        self._make_label(tab, "Repository URL")
        self.repo_url_entry = self._make_entry(tab, "https://github.com/owner/repo")

        # PR ID
        self._make_label(tab, "Pull Request ID")
        self.pr_id_entry = self._make_entry(tab, "e.g. 42")

        # LLM provider option
        self._make_label(tab, "LLM Provider")
        self.provider_menu = ctk.CTkOptionMenu(
            tab,
            values=["Gemini", "Ollama"],
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_PRIMARY,
            fg_color=BG_DARK,
            button_color=BORDER,
            button_hover_color=ACCENT,
            dropdown_fg_color=BG_DARK,
            dropdown_text_color=TEXT_PRIMARY,
            dropdown_hover_color=ACCENT,
            corner_radius=8,
        )
        self.provider_menu.pack(anchor="w", padx=20, pady=(0, 2))

        # PDF checkbox
        self.pdf_review_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            tab,
            text="Generate PDF report",
            variable=self.pdf_review_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            border_color=BORDER,
            corner_radius=6,
        ).pack(anchor="w", padx=20, pady=(14, 0))

        # Submit button
        ctk.CTkButton(
            tab,
            text="Review Pull Request",
            command=self._handle_pr_review,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=BG_DARK,
            height=42,
            corner_radius=10,
        ).pack(fill="x", padx=20, pady=(20, 0))

        # Progress bar (hidden by default)
        self.review_progress = ctk.CTkProgressBar(
            tab,
            fg_color=BG_DARK,
            progress_color=ACCENT,
            height=4,
            corner_radius=2,
        )
        self.review_progress.pack(fill="x", padx=20, pady=(8, 0))
        self.review_progress.configure(mode="indeterminate")
        self.review_progress.pack_forget()

        # Message area (below progress bar)
        self.review_message = ctk.CTkLabel(
            tab,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=SUCCESS,
            anchor="w",
        )
        self.review_message.pack(fill="x", padx=20, pady=(6, 0))
        self.review_message.pack_forget()

        # Separator
        self.review_separator = ctk.CTkFrame(
            tab,
            fg_color=BORDER,
            height=1,
        )
        self.review_separator.pack(fill="x", padx=20, pady=(10, 0))
        self.review_separator.pack_forget()

        # Scrollable results area
        self.review_results = ctk.CTkScrollableFrame(
            tab,
            fg_color=BG_DARK,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
        )
        self.review_results.pack(fill="both", expand=True, padx=20, pady=(10, 10))
        self.review_results.pack_forget()

    # ─────────────────────────────────────────────────────────
    #  Tab 2 – Saved Feedback
    # ─────────────────────────────────────────────────────────
    def _build_feedback_tab(self):
        tab = self.tab_feedback
        tab.configure(fg_color=BG_CARD)

        # Date range – from
        self._make_label(tab, "From")
        range_from = ctk.CTkFrame(tab, fg_color="transparent")
        range_from.pack(fill="x", padx=20, pady=(0, 4))

        self.from_month_entry = self._make_inline_entry(range_from, "Month (1-12)", 0)
        self.from_year_entry = self._make_inline_entry(range_from, "Year", 1)

        # Date range – until
        self._make_label(tab, "Until")
        range_until = ctk.CTkFrame(tab, fg_color="transparent")
        range_until.pack(fill="x", padx=20, pady=(0, 4))

        self.until_month_entry = self._make_inline_entry(range_until, "Month (1-12)", 0)
        self.until_year_entry = self._make_inline_entry(range_until, "Year", 1)

        # PDF checkbox
        self.pdf_feedback_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            tab,
            text="Generate PDF report",
            variable=self.pdf_feedback_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_PRIMARY,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            border_color=BORDER,
            corner_radius=6,
        ).pack(anchor="w", padx=20, pady=(14, 0))

        # Submit button
        ctk.CTkButton(
            tab,
            text="Display Saved Feedback",
            command=self._handle_display_feedback,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=BG_DARK,
            height=42,
            corner_radius=10,
        ).pack(fill="x", padx=20, pady=(20, 0))

        # Progress bar (hidden by default)
        self.feedback_progress = ctk.CTkProgressBar(
            tab,
            fg_color=BG_DARK,
            progress_color=ACCENT,
            height=4,
            corner_radius=2,
        )
        self.feedback_progress.pack(fill="x", padx=20, pady=(8, 0))
        self.feedback_progress.configure(mode="indeterminate")
        self.feedback_progress.pack_forget()

        # Message area
        self.feedback_message = ctk.CTkLabel(
            tab,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=SUCCESS,
            anchor="w",
        )
        self.feedback_message.pack(fill="x", padx=20, pady=(6, 0))
        self.feedback_message.pack_forget()

        # Separator
        self.feedback_separator = ctk.CTkFrame(
            tab,
            fg_color=BORDER,
            height=1,
        )
        self.feedback_separator.pack(fill="x", padx=20, pady=(10, 0))
        self.feedback_separator.pack_forget()

        # Scrollable results area
        self.feedback_results = ctk.CTkScrollableFrame(
            tab,
            fg_color=BG_DARK,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
        )
        self.feedback_results.pack(fill="both", expand=True, padx=20, pady=(10, 10))
        self.feedback_results.pack_forget()

    # ─────────────────────────────────────────────────────────
    #  Tab 3 – Analyze Repo
    # ─────────────────────────────────────────────────────────
    def _build_analyze_tab(self):
        tab = self.tab_analyze
        tab.configure(fg_color=BG_CARD)

        # Repo URL
        self._make_label(tab, "Repository URL")
        self.analyze_url_entry = self._make_entry(tab, "https://github.com/owner/repo")

        # LLM provider option
        self._make_label(tab, "LLM Provider")
        self.provider_menu = ctk.CTkOptionMenu(
            tab,
            values=["Gemini", "Ollama"],
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=TEXT_PRIMARY,
            fg_color=BG_DARK,
            button_color=BORDER,
            button_hover_color=ACCENT,
            dropdown_fg_color=BG_DARK,
            dropdown_text_color=TEXT_PRIMARY,
            dropdown_hover_color=ACCENT,
            corner_radius=8,
        )
        self.provider_menu.pack(anchor="w", padx=20, pady=(0, 2))

        # Submit button
        ctk.CTkButton(
            tab,
            text="Analyze Repository History",
            command=self._handle_repo_history,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=BG_DARK,
            height=42,
            corner_radius=10,
        ).pack(fill="x", padx=20, pady=(20, 0))

        # Progress bar (hidden by default)
        self.analyze_progress = ctk.CTkProgressBar(
            tab,
            fg_color=BG_DARK,
            progress_color=ACCENT,
            height=4,
            corner_radius=2,
        )
        self.analyze_progress.pack(fill="x", padx=20, pady=(8, 0))
        self.analyze_progress.configure(mode="indeterminate")
        self.analyze_progress.pack_forget()

        # Message area (below progress bar)
        self.analyze_message = ctk.CTkLabel(
            tab,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=SUCCESS,
            anchor="w",
        )
        self.analyze_message.pack(fill="x", padx=20, pady=(6, 0))
        self.analyze_message.pack_forget()

        # Separator
        self.analyze_separator = ctk.CTkFrame(
            tab,
            fg_color=BORDER,
            height=1,
        )
        self.analyze_separator.pack(fill="x", padx=20, pady=(10, 0))
        self.analyze_separator.pack_forget()

        # Scrollable results area
        self.analyze_results = ctk.CTkScrollableFrame(
            tab,
            fg_color=BG_DARK,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
        )
        self.analyze_results.pack(fill="both", expand=True, padx=20, pady=(10, 10))
        self.analyze_results.pack_forget()

    # ─────────────────────────────────────────────────────────
    #  Widget helpers
    # ─────────────────────────────────────────────────────────
    def _make_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(anchor="w", padx=20, pady=(14, 4))

    def _make_entry(self, parent, placeholder):
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=BG_DARK,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_DIM,
            border_color=BORDER,
            corner_radius=8,
            height=38,
        )
        entry.pack(fill="x", padx=20, pady=(0, 2))
        return entry

    def _make_inline_entry(self, parent, placeholder, column):
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=BG_DARK,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_DIM,
            border_color=BORDER,
            corner_radius=8,
            height=38,
        )
        entry.grid(row=0, column=column, sticky="ew", padx=(0, 10) if column == 0 else (0, 0))
        parent.columnconfigure(column, weight=1)
        return entry

    # ─────────────────────────────────────────────────────────
    #  Button handlers
    # ─────────────────────────────────────────────────────────
    def _handle_pr_review(self):
        repo_url = self.repo_url_entry.get().strip()
        pr_id_text = self.pr_id_entry.get().strip()

        if not repo_url or not pr_id_text:
            self._set_status("Please fill in all fields.", error=True)
            return

        try:
            pr_id = [int(pr_id_text)]
        except ValueError:
            self._set_status("PR ID must be a number.", error=True)
            return

        is_pdf = self.pdf_review_var.get()
        provider = self.provider_menu.get().lower()

        # show progress bar
        self._show_progress("review")
        self._set_status("Reviewing pull request — this may take a few minutes...")

        self._run_in_thread(
            [repo_url, pr_id, provider], 1, is_pdf
        )

    def _handle_display_feedback(self):
        try:
            from_month = int(self.from_month_entry.get())
            until_month = int(self.until_month_entry.get())
            from_year = int(self.from_year_entry.get())
            until_year = int(self.until_year_entry.get())
        except ValueError:
            self._set_status("Please enter valid numbers for all date fields.", error=True)
            return

        is_pdf = self.pdf_feedback_var.get()

        # show progress bar
        self._show_progress("feedback")
        self._set_status("Loading saved feedback...")

        self._run_in_thread(
            [from_month, until_month, from_year, until_year], 2, is_pdf
        )

    def _handle_repo_history(self):
        repo_url = self.analyze_url_entry.get().strip()

        if not repo_url:
            self._set_status("Please enter a repository URL.", error=True)
            return

        is_pdf = False
        provider = self.provider_menu.get().lower()

        self._show_progress("analyze")
        self._set_status("Analyzing repository history...")

        self._run_in_thread(
            [repo_url, provider], 3, is_pdf
        )

    # ─────────────────────────────────────────────────────────
    #  Execute pipeline (threaded so UI doesn't freeze)
    # ─────────────────────────────────────────────────────────
    def _run_in_thread(self, args, pipeline_type, is_pdf):
        def task():
            try:
                self.controller.run(args, pipeline_type, is_pdf)
                self.after(0, lambda: self._set_status("Done!", success=True))
            except Exception as e:
                tab = (
                    "review" if pipeline_type == 1 else
                    "feedback" if pipeline_type == 2 else
                    "analyze"
                )

                self.after(0, lambda t=tab: self._hide_progress(t))
                self.after(0, lambda err=e: self._set_status(f"Error: {err}", error=True))
                #self.after(0, lambda: self._hide_progress(tab))
                #self.after(0, lambda: self._set_status(f"Error: {e}", error=True))

        thread = threading.Thread(target=task, daemon=True)
        thread.start()

    # ─────────────────────────────────────────────────────────
    #  Progress bar helpers
    # ─────────────────────────────────────────────────────────
    def _show_progress(self, tab_name):
        if tab_name == "review":
            self.review_progress.pack(fill="x", padx=20, pady=(8, 0))
            self.review_progress.start()
        elif tab_name == "feedback":
            self.feedback_progress.pack(fill="x", padx=20, pady=(8, 0))
            self.feedback_progress.start()
        else:
            self.analyze_progress.pack(fill="x", padx=20, pady=(8, 0))
            self.analyze_progress.start()

    def _hide_progress(self, tab_name):
        if tab_name == "review":
            self.review_progress.stop()
            self.review_progress.pack_forget()
        elif tab_name == "feedback":
            self.feedback_progress.stop()
            self.feedback_progress.pack_forget()
        else:
            self.analyze_progress.stop()
            self.analyze_progress.pack_forget()

    # ─────────────────────────────────────────────────────────
    #  Display results in scrollable area
    # ─────────────────────────────────────────────────────────
    def _display_results(self, output_list, tab_name):
        if tab_name == "review":
            results_frame = self.review_results
            message_label = self.review_message
            separator = self.review_separator
        else:
            results_frame = self.feedback_results
            message_label = self.feedback_message
            separator = self.feedback_separator

        # hide progress bar
        self._hide_progress(tab_name)

        # clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        # show message, separator, and results area
        message_label.pack(fill="x", padx=20, pady=(6, 0))
        separator.pack(fill="x", padx=20, pady=(10, 0))
        results_frame.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # build results for each output
        for output in output_list:
            pr_info = output.get_pr_info()
            feedback = output.get_feedback_output()

            # PR header
            ctk.CTkLabel(
                results_frame,
                text=f"PR #{pr_info.get_id()}: {pr_info.get_title()}",
                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                text_color=ACCENT,
                anchor="w",
            ).pack(fill="x", padx=10, pady=(12, 2))

            ctk.CTkLabel(
                results_frame,
                text=f"Repository: {pr_info.get_repo_info().get_repo_name()}",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=TEXT_DIM,
                anchor="w",
            ).pack(fill="x", padx=10, pady=(0, 8))

            errors = feedback.get_all_errors()

            if not errors:
                ctk.CTkLabel(
                    results_frame,
                    text="No errors found.",
                    font=ctk.CTkFont(family="Segoe UI", size=13),
                    text_color=SUCCESS,
                    anchor="w",
                ).pack(fill="x", padx=10, pady=(4, 10))
                continue

            # display each error in a card
            for error in errors:
                self._make_error_card(results_frame, error)

    def _display_results_3(self, analysis_list: list[Analysis]):
        results_frame = self.analyze_results
        message_label = self.analyze_message
        separator = self.analyze_separator

        # hide progress bar
        self._hide_progress("analyze")

        # clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        # show UI elements
        message_label.pack(fill="x", padx=20, pady=(6, 0))
        separator.pack(fill="x", padx=20, pady=(10, 0))
        results_frame.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # build results
        for analysis_obj in analysis_list:
            commit_id = analysis_obj.get_commit_id()
            filename = analysis_obj.get_filename()
            analysis_text = analysis_obj.get_analysis()

            if analysis_text:
                try:
                    parsed = json.loads(analysis_text)
                    display_text = parsed.get("analysis", analysis_text)
                except (json.JSONDecodeError, TypeError):
                    display_text = analysis_text
            else:
                display_text = "No analysis available."

            self._make_analysis_card(results_frame, commit_id, filename, display_text)

    def _make_error_card(self, parent, error):
        """Creates a styled card for a single error."""
        card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
        )
        card.pack(fill="x", padx=10, pady=(0, 8))

        # error type and severity on same row
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            header,
            text=error.get_error_type(),
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        # color-code severity
        severity = error.get_error_severity_level()
        severity_color = self._get_severity_color(severity)

        ctk.CTkLabel(
            header,
            text=severity.upper(),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=severity_color,
        ).pack(side="right")

        # description
        ctk.CTkLabel(
            card,
            text=error.get_error_description(),
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_PRIMARY,
            anchor="w",
            justify="left",
            wraplength=600,
        ).pack(fill="x", padx=12, pady=(0, 6))

        # suggestion
        suggestion = error.get_fix_suggestion()
        if suggestion:
            ctk.CTkLabel(
                card,
                text="Suggestion:",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=ACCENT,
                anchor="w",
            ).pack(fill="x", padx=12, pady=(2, 0))

            ctk.CTkLabel(
                card,
                text=suggestion,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=TEXT_DIM,
                anchor="w",
                justify="left",
                wraplength=600,
            ).pack(fill="x", padx=12, pady=(0, 10))

    def _make_analysis_card(self, parent, commit_id, filename, analysis_text):
        """Creates a styled card for a single error."""
        card = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=8,
        )
        card.pack(fill="x", padx=10, pady=(0, 8))

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 4))

        ctk.CTkLabel(
            header,
            text=commit_id,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        ctk.CTkLabel(
            card,
            text=f"File: {filename}",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=TEXT_DIM,
            anchor="w",
        ).pack(fill="x", padx=12, pady=(0, 4))

        # description
        ctk.CTkLabel(
            card,
            text=analysis_text,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=TEXT_PRIMARY,
            anchor="w",
            justify="left",
            wraplength=600,
        ).pack(fill="x", padx=12, pady=(0, 6))

    def _get_severity_color(self, severity):
        severity = severity.lower()
        if severity in ("severe", "high"):
            return DANGER
        elif severity == "medium":
            return WARNING
        else:
            return SUCCESS

    # ─────────────────────────────────────────────────────────
    #  Status bar helper
    # ─────────────────────────────────────────────────────────
    def _set_status(self, message, error=False, success=False):
        if error:
            color = DANGER
        elif success:
            color = SUCCESS
        else:
            color = TEXT_DIM
        self.status_label.configure(text=message, text_color=color)

    # ─────────────────────────────────────────────────────────
    #  Receive output from controller
    # ─────────────────────────────────────────────────────────
    def receive_output_1(self, output_list):
        self.after(0, lambda: self._on_review_complete(output_list))

    def receive_output_2(self, outputs_list):
        # flatten the list of lists into one list
        flat_list = []
        for group in outputs_list:
            if isinstance(group, list):
                flat_list.extend(group)
            else:
                flat_list.append(group)
        self.after(0, lambda: self._on_feedback_complete(flat_list))

    def receive_output_3(self, analysis_list: list[Analysis]):
        self.after(0, lambda: self._on_repo_analysis_complete(analysis_list))

    def _on_review_complete(self, output_list):
        # show PDF path message if applicable
        if self.pdf_review_var.get() and output_list:
            self.review_message.configure(
                text="PDF report saved successfully.",
                text_color=SUCCESS,
            )
        else:
            self.review_message.configure(
                text="Review complete.",
                text_color=SUCCESS,
            )

        self._display_results(output_list, "review")
        self._set_status("Done!", success=True)

    def _on_feedback_complete(self, output_list):
        if self.pdf_feedback_var.get() and output_list:
            self.feedback_message.configure(
                text="PDF report saved successfully.",
                text_color=SUCCESS,
            )
        else:
            self.feedback_message.configure(
                text="Feedback loaded.",
                text_color=SUCCESS,
            )

        self._display_results(output_list, "feedback")
        self._set_status("Done!", success=True)

    def _on_repo_analysis_complete(self, analysis_list: list[Analysis]):
        self.analyze_message.configure(
            text="Analysis complete.",
            text_color=SUCCESS,
        )

        self._display_results_3(analysis_list)
        self._set_status("Done!", success=True)
