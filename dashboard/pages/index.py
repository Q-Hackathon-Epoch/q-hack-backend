import datetime

import reflex as rx

from .. import styles
from ..components.card import card
from ..templates import template
from ..views.charts import (
    StatsState,
    area_toggle,
)
from ..views.stats_cards import stats_cards
from dashboard.backend.upload_state import trigger_pipeline


class State(rx.State):
    problems: str = ""
    goals: str = ""
    weaknesses: str = ""
    strength: str = ""
    modules_filename: str = ""
    transcript_filename: str = ""
    skills_filename: str = ""
    progress: int = 0  # For progress tracking

    def calculate_progress(self) -> int:
        """Calculate completion progress based on filled fields"""
        total_items = 7  # 3 files + 4 text fields
        filled_items = 0

        # Check file uploads
        if self.modules_filename:
            filled_items += 1
        if self.transcript_filename:
            filled_items += 1
        if self.skills_filename:
            filled_items += 1

        # Check text fields
        if self.problems:
            filled_items += 1
        if self.goals:
            filled_items += 1
        if self.weaknesses:
            filled_items += 1
        if self.strength:
            filled_items += 1

        return int((filled_items / total_items) * 100)

    async def reset_all(self):
        self.problems = ""
        self.goals = ""
        self.weaknesses = ""
        self.strength = ""
        self.modules_filename = ""
        self.transcript_filename = ""
        self.skills_filename = ""
        self.progress = 0

    async def handle_submit(self):
        if (
            not self.modules_filename
            or not self.transcript_filename
            or not self.skills_filename
            or not self.problems
            or not self.goals
            or not self.weaknesses
            or not self.strength
        ):
            return rx.window_alert(
                "Please complete all fields before submitting"
            )

        content = (
            f"Problems: {self.problems}\n"
            f"Goals: {self.goals}\n"
            f"Weaknesses: {self.weaknesses}\n"
            f"Strength: {self.strength}\n"
        )
        upload_dir = rx.get_upload_dir()
        filename = "students-self-description.txt"
        outfile = upload_dir / filename
        with outfile.open("w", encoding="utf-8") as f:
            f.write(content)
        print(f"Form data saved to {filename}")
        trigger_pipeline()
        return rx.redirect("/jobs")

    async def _handle_upload_and_set_name(self, files, kind):
        await self.handle_upload(files, kind)
        if isinstance(files, list) and files:
            item = files[0]
        else:
            item = files
        if hasattr(item, "filename"):
            name = item.filename
        else:
            name = f"{kind}.pdf"

        if kind == "module_handbook":
            self.modules_filename = name
        elif kind == "grade_sheet":
            self.transcript_filename = name
        elif kind == "student_cv":
            self.skills_filename = name

        # Update progress when a file is uploaded
        self.progress = self.calculate_progress()

    async def handle_upload_modules(self, files):
        await self._handle_upload_and_set_name(files, "module_handbook")

    async def handle_upload_transcript(self, files):
        await self._handle_upload_and_set_name(files, "grade_sheet")

    async def handle_upload_skills(self, files):
        await self._handle_upload_and_set_name(files, "student_cv")

    async def handle_upload(self, files, kind):
        try:
            if isinstance(files, list):
                for file in files:
                    if hasattr(file, "read"):
                        upload_data = await file.read()
                        filename = file.filename
                    else:
                        upload_data = file
                        filename = f"{kind}.pdf"
                    outfile = rx.get_upload_dir() / filename
                    with outfile.open("wb") as file_object:
                        file_object.write(upload_data)
                    print(f"The file {filename} was uploaded")
                    # print(kind)
                    # if kind == "module_handbook":
                    #     ProcessingState.modules_path = './uploaded_files/' + filename #update_modules_response('./uploaded_files/' + filename)
                    # elif kind == "grade_sheet":
                    #     ProcessingState.grades_path = './uploaded_files/' + filename #update_grades_response('./uploaded_files/' + filename)
                    # elif kind == "student_cv":
                    #     pass
            else:
                file = files
                if hasattr(file, "read"):
                    upload_data = await file.read()
                    filename = file.filename
                else:
                    upload_data = file
                    filename = f"{kind}.pdf"
                outfile = rx.get_upload_dir() / filename
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)
                print(f"The file {filename} was uploaded")
        except Exception as e:
            print(f"Error in handle_upload: {type(e).__name__}: {e}")

    async def update_text_field(self, value, field_name):
        setattr(self, field_name, value)
        self.progress = self.calculate_progress()


@template(
    route="/",
    title="Let's Get To Know You Better",
    on_load=[State.reset_all],
)
def index() -> rx.Component:
    return rx.vstack(
        # Sticky progress bar container
        rx.box(
            rx.progress(
                value=State.progress,
                width="100%",
                color_scheme="green",
                height="0.5rem",
                border_radius="md",
            ),
            rx.text(
                f"{State.progress}% Complete",
                size="2",
                align="right",
                margin_top="0.25rem",
            ),
            width="100%",
            padding="1rem",  # Add padding inside the sticky box
            position="sticky",
            top="0",
            z_index="10",
            background_color=rx.color("gray", 1),  # Add background color
            box_shadow="0 2px 4px rgba(0,0,0,0.1)",  # Add shadow
            margin_bottom="1rem",  # Add some margin below the sticky bar
        ),
        # Main content area
        rx.vstack(
            rx.heading(
                "Let's Get To Know You Better", size="8", margin_bottom="2rem"
            ),
            rx.text(
                "Please provide the following information to help us create a personalized roadmap for your academic and career journey.",
                size="4",
                color="gray",
                margin_bottom="2rem",
                text_align="center",
            ),
            rx.form(
                rx.vstack(
                    # Upload section
                    rx.vstack(
                        # Module Handbook Upload
                        card(
                            rx.vstack(
                                rx.heading(
                                    "University Module Handbook",
                                    size="6",
                                    margin_bottom="1rem",
                                ),
                                rx.text(
                                    "Please upload your university's module handbook to help us understand what courses are available.",
                                    size="3",
                                    color="gray",
                                ),
                                rx.upload(
                                    rx.cond(
                                        State.modules_filename != "",
                                        rx.hstack(
                                            rx.icon("check", color="green"),
                                            rx.text(
                                                State.modules_filename,
                                                color="green",
                                            ),
                                            align="center",
                                        ),
                                        rx.hstack(
                                            rx.icon("upload", color="gray"),
                                            rx.text(
                                                "Drag & drop module handbook or click to browse"
                                            ),
                                            align="center",
                                        ),
                                    ),
                                    id="upload_modules",
                                    accept={
                                        "application/pdf": [".pdf"],
                                        "text/html": [".html", ".htm"],
                                    },
                                    on_drop=State.handle_upload_modules,
                                    max_files=1,
                                    height="100px",
                                    width="100%",
                                    border="2px dashed",
                                    border_color="gray.200",
                                    border_radius="md",
                                    padding="1rem",
                                ),
                                align_items="start",
                                width="100%",
                            ),
                        ),
                        # Grade Sheet Upload
                        card(
                            rx.vstack(
                                rx.heading(
                                    "Academic Transcript/Grade Sheet",
                                    size="6",
                                    margin_bottom="1rem",
                                ),
                                rx.text(
                                    "Share your current grades to help us understand what modules you've completed.",
                                    size="3",
                                    color="gray",
                                ),
                                rx.upload(
                                    rx.cond(
                                        State.transcript_filename != "",
                                        rx.hstack(
                                            rx.icon("check", color="green"),
                                            rx.text(
                                                State.transcript_filename,
                                                color="green",
                                            ),
                                            align="center",
                                        ),
                                        rx.hstack(
                                            rx.icon("upload", color="gray"),
                                            rx.text(
                                                "Drag & drop grade sheet or click to browse"
                                            ),
                                            align="center",
                                        ),
                                    ),
                                    id="upload_transcript",
                                    accept={
                                        "application/pdf": [".pdf"],
                                        "text/html": [".html", ".htm"],
                                    },
                                    on_drop=State.handle_upload_transcript,
                                    max_files=1,
                                    height="100px",
                                    width="100%",
                                    border="2px dashed",
                                    border_color="gray.200",
                                    border_radius="md",
                                    padding="1rem",
                                ),
                                align_items="start",
                                width="100%",
                            )
                        ),
                        # CV/LinkedIn Upload
                        card(
                            rx.vstack(
                                rx.heading(
                                    "Your Skills & Experience",
                                    size="6",
                                    margin_bottom="1rem",
                                ),
                                rx.text(
                                    "Upload your CV or LinkedIn profile export to help us understand your background.",
                                    size="3",
                                    color="gray",
                                ),
                                rx.upload(
                                    rx.cond(
                                        State.skills_filename != "",
                                        rx.hstack(
                                            rx.icon("check", color="green"),
                                            rx.text(
                                                State.skills_filename,
                                                color="green",
                                            ),
                                            align="center",
                                        ),
                                        rx.hstack(
                                            rx.icon("upload", color="gray"),
                                            rx.text(
                                                "Drag & drop CV/LinkedIn export or click to browse"
                                            ),
                                            align="center",
                                        ),
                                    ),
                                    id="upload_skills",
                                    accept={
                                        "application/pdf": [".pdf"],
                                        "text/html": [".html", ".htm"],
                                    },
                                    on_drop=State.handle_upload_skills,
                                    max_files=1,
                                    height="100px",
                                    width="100%",
                                    border="2px dashed",
                                    border_color="gray.200",
                                    border_radius="md",
                                    padding="1rem",
                                ),
                                align_items="start",
                                width="100%",
                            )
                        ),
                        width="100%",
                        spacing="8",
                    ),
                    # Self-description section
                    card(
                        rx.vstack(
                            rx.heading(
                                "Tell Us About Yourself",
                                size="6",
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Please share your strengths, weaknesses, goals, and any challenges you're facing.",
                                size="3",
                                color="gray",
                                margin_bottom="1rem",
                            ),
                            rx.text_area(
                                placeholder="Describe your career goals and aspirations...",
                                value=State.goals,
                                on_change=lambda value: State.update_text_field(
                                    value, "goals"
                                ),
                                height="100px",
                                width="100%",
                                margin_bottom="1rem",
                            ),
                            rx.text_area(
                                placeholder="Describe your strengths...",
                                value=State.strength,
                                on_change=lambda value: State.update_text_field(
                                    value, "strength"
                                ),
                                height="100px",
                                width="100%",
                                margin_bottom="1rem",
                            ),
                            rx.text_area(
                                placeholder="Describe areas you'd like to improve...",
                                value=State.weaknesses,
                                on_change=lambda value: State.update_text_field(
                                    value, "weaknesses"
                                ),
                                height="100px",
                                width="100%",
                                margin_bottom="1rem",
                            ),
                            rx.text_area(
                                placeholder="Describe any challenges you're facing in your academic or career journey...",
                                value=State.problems,
                                on_change=lambda value: State.update_text_field(
                                    value, "problems"
                                ),
                                height="100px",
                                width="100%",
                            ),
                            align_items="start",
                            width="100%",
                        ),
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon("arrow-right"),
                            rx.text("Let's Go!"),
                        ),
                        type="submit",
                        width="200px",
                        color_scheme="green",
                        size="3",
                        margin_top="2rem",
                    ),
                    width="100%",
                    max_width="800px",
                    margin="auto",
                    spacing="8",
                    padding="1rem",
                ),
                on_submit=State.handle_submit,
                width="100%",
            ),
            width="100%",
            padding="2rem",  # Keep padding for the main content
            spacing="4",
        ),
        width="100%",
        align_items="center",  # Center align items in the outer vstack
        spacing="0",  # Remove spacing from outer vstack to avoid gap below sticky bar
    )
