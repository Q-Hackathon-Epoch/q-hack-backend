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

class State(rx.State):
    """The app state."""

    # The images to show.
    img: list[str]

    @rx.event
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

            # Update the img var.
            self.img.append(file.filename)


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
        rx.grid(
            card(
                rx.heading("Please tell us about your Uni Modules", mb='5em'),
                rx.upload(
                            rx.vstack(
                                rx.button(
                                    "Select File",
                                    color="red",
                                    bg="white",
                                    border=f"1px solid red",
                                    box_shadow=styles.box_shadow_style,
                                ),
                                rx.text(
                                    "Drag and drop files here or click to select files"
                                ),
                            ),
                            id="upload1",
                            border=f"1px dotted red",
                            padding="5em",
                        ),
                        rx.hstack(
                            rx.foreach(
                                rx.selected_files("upload1"), rx.text
                            )
                        ),
                        rx.button(
                            "Upload",
                            on_click=State.handle_upload(
                                rx.upload_files(upload_id="upload1")
                            ),
                        ),
                        rx.button(
                            "Clear",
                            on_click=rx.clear_selected_files("upload1"),
                        ),
                        rx.foreach(
                            State.img,
                            lambda img: rx.image(
                                src=rx.get_upload_url(img)
                            ),
                        )
            ),
            card(
                rx.hstack(
                    rx.icon("globe", size=20),
                    rx.text("Acquisition Overview", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                    margin_bottom="2.5em",
                ),
                rx.vstack(
                    acquisition(),
                ),
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
            ],
            width="100%",
        ),
        spacing="8",
        width="100%",
    )
