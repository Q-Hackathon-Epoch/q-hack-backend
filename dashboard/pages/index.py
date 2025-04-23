"""The overview page of the app."""

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
from .profile import ProfileState


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

import datetime
import reflex as rx


class State(rx.State):
    """The app state."""

    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
                print(f"The file {file.filename} was uploaded")




@template(route="/", title="Overview", on_load=StatsState.randomize_data)
def index() -> rx.Component:
    """The overview page.

    Returns:
        The UI for the overview page.

    """
    return rx.vstack(
        rx.heading(f"Let's Get To Know You Better", size="9"),
        # rx.flex(
        #     rx.input(
        #         rx.input.slot(rx.icon("search"), padding_left="0"),
        #         placeholder="Search here...",
        #         size="3",
        #         width="100%",
        #         max_width="450px",
        #         radius="large",
        #         style=styles.ghost_input_style,
        #     ),
        #     rx.flex(
        #         notification("bell", "cyan", 12),
        #         notification("message-square-text", "plum", 6),
        #         spacing="4",
        #         width="100%",
        #         wrap="nowrap",
        #         justify="end",
        #     ),
        #     justify="between",
        #     align="center",
        #     width="100%",
        # ),
        # stats_cards(),
        # card(
        #     rx.hstack(
        #         tab_content_header(),
        #         rx.segmented_control.root(
        #             rx.segmented_control.item("Users", value="users"),
        #             rx.segmented_control.item("Revenue", value="revenue"),
        #             rx.segmented_control.item("Orders", value="orders"),
        #             margin_bottom="1.5em",
        #             default_value="users",
        #             on_change=StatsState.set_selected_tab,
        #         ),
        #         width="100%",
        #         justify="between",
        #     ),
        #     rx.match(
        #         StatsState.selected_tab,
        #         ("users", users_chart()),
        #         ("revenue", revenue_chart()),
        #         ("orders", orders_chart()),
        #     ),
        # ),
        rx.form(
            rx.flex(
            card(
                rx.upload(
                    rx.text("Drag & drop your Module Handbook [pdf, html]"),
                    id="upload_modules",
                    accept={
                        "application/pdf": [".pdf"],
                        "text/html": [".html", ".htm"],
                    },
                    on_drop=State.handle_upload(
                        rx.upload_files(upload_id="upload_file_modules")
                    ),
                    max_files=1,
                ),
            ),
            card(
                rx.upload(
                    rx.text("Drag & drop your academic transcript [pdf, html]"),
                    id="upload_transcript",
                    accept={
                        "application/pdf": [".pdf"],
                        "text/html": [".html", ".htm"],
                    },
                    on_drop=State.handle_upload(
                        rx.upload_files(upload_id="upload_file_modules")
                    ),
                    max_files=1,
                ),
            ),
            card(
                rx.upload(
                    rx.text("Drag & drop your LinkedIn / GitHub snapshot [pdf, html]"),
                    id="upload_skills",
                    accept={
                        "application/pdf": [".pdf"],
                        "text/html": [".html", ".htm"],
                    },
                    on_drop=State.handle_upload(
                        rx.upload_files(upload_id="upload_file_modules")
                    ),
                    max_files=1,
                
                ),
            ),
            card(
                rx.flex(
                    rx.input(name="problems",    placeholder="Your problems",    width="100%"),
                    rx.input(name="goals",       placeholder="Your goals",       width="100%"),
                    rx.input(name="weaknesses",  placeholder="Your weaknesses",  width="100%"),
                    rx.input(name="strength",    placeholder="Your strength",    width="100%"),
                    gap="1rem", direction="column",
                ),
            ),
            rx.button("Submit", type="submit", margin_top="1rem"),
            gap="1rem",
            direction="column",
            align="center",
            width='40rem',
            margin='auto',
            ),
        ),
        spacing="8",
        width="100%",
    )