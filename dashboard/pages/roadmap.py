"""The table page."""

import reflex as rx

from ..templates import template
from ..views.table import main_table


@template(
    route="/roadmap", title="Your Roadmaps",
)
def Roadmap() -> rx.Component:
    """The table page.

    Returns:
        The UI for the table page.

    """
    return rx.vstack(
        rx.heading("Table", size="5"),
        main_table(),
        spacing="8",
        width="100%",
    )
