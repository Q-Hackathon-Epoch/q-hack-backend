import datetime

import reflex as rx

from .. import styles
from ..components.card import card
from ..components.notification import notification
from ..templates import template
from ..views.acquisition_view import acquisition
from ..views.charts import (
    StatsState,
    area_toggle,
    orders_chart,
    pie_chart,
    revenue_chart,
    timeframe_select,
    users_chart,
)
from ..views.stats_cards import stats_cards
from .interview import ProfileState


def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%b %d, %Y')} - {datetime.datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Last 30 days", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )


def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )


class State(rx.State):
    problems: str = ""
    goals: str = ""
    weaknesses: str = ""
    strength: str = ""
    modules_filename: str = ""
    transcript_filename: str = ""
    skills_filename: str = ""

    async def reset_all(self):
        self.problems = ""
        self.goals = ""
        self.weaknesses = ""
        self.strength = ""
        self.modules_filename = ""
        self.transcript_filename = ""
        self.skills_filename = ""

    async def handle_submit(self):
        content = (
            f"Problems: {self.problems}\n"
            f"Goals: {self.goals}\n"
            f"Weaknesses: {self.weaknesses}\n"
            f"Strength: {self.strength}\n"
        )
        upload_dir = rx.get_upload_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = "students-self-description.txt"
        outfile = upload_dir / filename
        with outfile.open("w", encoding="utf-8") as f:
            f.write(content)
        print(f"Form data saved to {filename}")
        return rx.redirect("/dashboard")

    async def handle_upload(self, files):
        print(f"Received upload: {type(files)}")
        try:
            if isinstance(files, list):
                for file in files:
                    if hasattr(file, "read"):
                        upload_data = await file.read()
                        filename = file.filename
                    else:
                        upload_data = file
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"upload_{timestamp}.pdf"
                    outfile = rx.get_upload_dir() / filename
                    with outfile.open("wb") as file_object:
                        file_object.write(upload_data)
                    print(f"The file {filename} was uploaded")
            else:
                file = files
                if hasattr(file, "read"):
                    upload_data = await file.read()
                    filename = file.filename
                else:
                    upload_data = file
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"upload_{timestamp}.pdf"
                outfile = rx.get_upload_dir() / filename
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)
                print(f"The file {filename} was uploaded")
        except Exception as e:
            print(f"Error in handle_upload: {type(e).__name__}: {e}")

    async def _handle_upload_and_set_name(self, files, kind):
        await self.handle_upload(files)
        if isinstance(files, list):
            item = files[0]
        else:
            item = files
        if hasattr(item, "filename"):
            name = item.filename
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"upload_{timestamp}.pdf"
        if kind == "modules":
            self.modules_filename = name
        elif kind == "transcript":
            self.transcript_filename = name
        elif kind == "skills":
            self.skills_filename = name

    async def handle_upload_modules(self, files):
        await self._handle_upload_and_set_name(files, "modules")

    async def handle_upload_transcript(self, files):
        await self._handle_upload_and_set_name(files, "transcript")

    async def handle_upload_skills(self, files):
        await self._handle_upload_and_set_name(files, "skills")


# @template(route="/", title="Overview", on_load=StatsState.randomize_data)
@template(
    route="/",
    title="Upload Your Data",
    on_load=[StatsState.randomize_data, State.reset_all],
)
def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Let's Get To Know You Better", size="9"),
        rx.form(
            rx.flex(
                card(
                    rx.upload(
                        rx.cond(
                            State.modules_filename != "",
                            rx.text(State.modules_filename, color="green"),
                            rx.text("Drag & drop your Module Handbook [pdf, html]"),
                        ),
                        id="upload_modules",
                        accept={
                            "application/pdf": [".pdf"],
                            "text/html": [".html", ".htm"],
                        },
                        on_drop=State.handle_upload_modules,
                        max_files=1,
                    ),
                ),
                card(
                    rx.upload(
                        rx.cond(
                            State.transcript_filename != "",
                            rx.text(State.transcript_filename+ "Click to change", color="green"),
                            rx.text("Drag & drop your academic transcript [pdf, html]"),
                        ),
                        id="upload_transcript",
                        accept={
                            "application/pdf": [".pdf"],
                            "text/html": [".html", ".htm"],
                        },
                        on_drop=State.handle_upload_transcript,
                        max_files=1,
                    ),
                ),
                card(
                    rx.upload(
                        rx.cond(
                            State.skills_filename != "",
                            rx.text(State.skills_filename, color="green"),
                            rx.text("Drag & drop your LinkedIn / GitHub snapshot [pdf, html]"),
                        ),
                        id="upload_skills",
                        accept={
                            "application/pdf": [".pdf"],
                            "text/html": [".html", ".htm"],
                        },
                        on_drop=State.handle_upload_skills,
                        max_files=1,
                    ),
                ),
                card(
                    rx.flex(
                        rx.input(
                            value=State.problems,
                            on_change=State.set_problems,
                            placeholder="Your problems",
                            width="100%",
                        ),
                        rx.input(
                            value=State.goals,
                            on_change=State.set_goals,
                            placeholder="Your goals",
                            width="100%",
                        ),
                        rx.input(
                            value=State.weaknesses,
                            on_change=State.set_weaknesses,
                            placeholder="Your weaknesses",
                            width="100%",
                        ),
                        rx.input(
                            value=State.strength,
                            on_change=State.set_strength,
                            placeholder="Your strength",
                            width="100%",
                        ),
                        gap="1rem",
                        direction="column",
                    ),
                ),
                rx.button("Submit", type="submit", margin_top="1rem"),
                gap="1rem",
                direction="column",
                align="center",
                width="40rem",
                margin="auto",
            ),
            on_submit=State.handle_submit,
        ),
        spacing="8",
        width="100%",
    )
