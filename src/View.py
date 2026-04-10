from typing import Any
import customtkinter as ctk
from datetime import date
import threading

"""
View class based on the MVC architecture.
CustomTkinter GUI replacement for Textual terminal UI.
"""

# ── Theme setup ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

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

class View(ctk.CTk):
    def __init__(self, controller: "Controller"):
        super().__init__()
        self.controller = controller

        # ── Window config ────────────────────────────────────
        self.title("Code Review With LLM")
        self.geometry("720x620")
        self.minsize(640, 560)
        self.configure(fg_color=BG_DARK)

        # ── Title bar ───────────────────────────────────────
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

        self._build_review_tab()
        self._build_feedback_tab()

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
            text_color="#1a1b26",
            height=42,
            corner_radius=10,
        ).pack(fill="x", padx=20, pady=(20, 10))

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
            text_color="#1a1b26",
            height=42,
            corner_radius=10,
        ).pack(fill="x", padx=20, pady=(20, 10))

    # ─────────────────────────────────────────────────────────
    #  Widget helpers (keep the build methods clean)
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
        ollama_model = "llama3:latest"

        self._set_status("Reviewing pull request — this may take a few minutes...")
        self._run_in_thread(
            [repo_url, pr_id, ollama_model], 1, is_pdf
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

        self._set_status("Loading saved feedback...")
        self._run_in_thread(
            [from_month, until_month, from_year, until_year], 2, is_pdf
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
                self.after(0, lambda: self._set_status(f"Error: {e}", error=True))

        thread = threading.Thread(target=task, daemon=True)
        thread.start()

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
    #  Receive output (called by controller — placeholders)
    # ─────────────────────────────────────────────────────────
    def receive_output_1(self, output_list):
        pass

    def receive_output_2(self, outputs_list):
        pass