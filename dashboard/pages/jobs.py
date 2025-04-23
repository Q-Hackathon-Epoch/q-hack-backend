"""The about page."""

from pathlib import Path

import reflex as rx

from .. import styles
from ..templates import template


@template(route="/jobs", title="Your jobs")
def Jobs() -> rx.Component:
    """The about page.

    Returns:
        The UI for the about page.
    """
    with Path("README.md").open(encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
