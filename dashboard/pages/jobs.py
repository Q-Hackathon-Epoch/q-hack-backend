"""The jobs page."""

import json
from pathlib import Path
from ..components.card import card

import reflex as rx

from ..templates import template


class State(rx.State):
    """Stores current filter option for the jobs page and matched job IDs."""

    # По умолчанию показываем "For you"
    filter_option: str = "match"
    # Пример списка подходящих вакансий по их ID
    matched_ids: list[int] = [1, 3, 7, 10]

    def set_filter(self, option: str):
        """Update selected filter option."""
        self.filter_option = option


# Путь к JSON с данными вакансий
DATA_PATH = Path(__file__).resolve().parent.parent / "test_data" / "jobs.json"


def _load_jobs() -> list[dict]:
    """Load jobs from the JSON file and normalize fields for rendering."""
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            jobs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    normalized = []
    for job in jobs:
        # Формируем отображаемые поля
        skills = job.get("skills", [])
        skills_str = ", ".join(skills)

        loc = job.get("location", {})
        location_str = ", ".join([loc.get("city", ""), loc.get("country", "")])

        sal = job.get("salary", {})
        min_s = sal.get("min")
        max_s = sal.get("max")
        curr = sal.get("currency", "")
        if min_s is not None and max_s is not None:
            salary_str = f"{min_s:,}–{max_s:,} {curr}"
        else:
            salary_str = ""

        remote_str = "Remote" if job.get("remote") else "On-site"

        pub_date = job.get("publication_date", "")
        pub_str = f"{pub_date}" if pub_date else ""

        normalized.append(
            {
                "id": job.get("id"),
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": location_str,
                "salary": salary_str,
                "type": job.get("employment_type", ""),
                "level": job.get("experience_level", ""),
                "industry": job.get("industry", ""),
                "skills_str": skills_str,
                "remote_str": remote_str,
                "pub_str": pub_str,
            }
        )
    return normalized


def _job_cards() -> rx.Component:
    """Grid of job cards wrapped in rx.card component with responsive layout."""
    jobs = _load_jobs()
    cards = []
    for job in jobs:
        show_var = (State.filter_option == "all") | (
            (State.filter_option == "match")
            & State.matched_ids.contains(job["id"])
        )

        # Build the card content
        content = rx.vstack(
            rx.image(
                src="/bg.png",
                width="100%",
                height="6em",
                object_fit="cover",
                position="absolute",
                left="0",
                top="0",
            ),
            rx.vstack(
                rx.text(
                    job["title"],
                    font_size="lg",
                    font_weight="bold",
                    no_of_lines=2,
                    margin_top="1rem",
                ),
                rx.text(job["company"], font_size="md"),
                rx.text(job["location"], font_size="sm"),
                rx.text(
                    f"💰 {job['salary']}",
                    font_size="sm",
                    font_weight="semibold",
                ),
                rx.hstack(
                    *[
                        rx.badge(ind.strip(), color_scheme="blue")
                        for ind in job["skills_str"].split(", ")[:2]
                    ],
                    wrap="wrap",
                    mt="2",
                ),
                # rx.text(f"Skills: {job['skills_str']}", font_size="xs", no_of_lines=2, mt="2"),
                rx.text(
                    job["pub_str"],
                    font_size="xxs",
                    align_self="flex-end",
                    mt="2",
                    position="absolute",
                    right="2",
                    bottom="0",
                ),
                spacing="2",
                padding="4",
                width="100%",
            ),
            spacing="0",
            width="100%",
        )

        # Wrap in rx.card for consistent styling
        card_wrapper = card(
            content,
            _hover={"transform": "scale(1.03)", "shadow": "md"},
            # overflow="hidden",
            padding_top="6em",
            padding="2",
            position="relative",
        )

        cards.append(rx.cond(show_var, card_wrapper, rx.fragment()))

    # Responsive grid template from example
    grid = rx.grid(
        *cards,
        gap="2rem",
        grid_template_columns=[
            "1fr",  # Mobile: 1 column
            "repeat(2, 1fr)",  # Tablet: 2 columns
            "repeat(3, 1fr)",  # Desktop: 3 columns
        ],
        width="100%",
        margin_top="1rem",
    )

    # Wrap grid in a centered box instead of container
    return rx.box(
        grid,
        max_width="1200px",
        mx="auto",
        px="4",
        width="full",
    )


@template(route="/jobs", title="Your Jobs")
def Jobs() -> rx.Component:
    """The jobs page component with filter controls."""
    return rx.vstack(
        rx.vstack(
            rx.heading("Let's find you a new job!", size="9"),
            rx.hstack(
                rx.cond(
                    State.filter_option == "match",
                    rx.text(
                        "For you",
                        font_weight="bold",
                        cursor="pointer",
                        on_click=State.set_filter("match"),
                    ),
                    rx.text(
                        "For you",
                        cursor="pointer",
                        on_click=State.set_filter("match"),
                    ),
                ),
                rx.cond(
                    State.filter_option == "all",
                    rx.text(
                        "All",
                        font_weight="bold",
                        cursor="pointer",
                        on_click=State.set_filter("all"),
                    ),
                    rx.text(
                        "All",
                        cursor="pointer",
                        on_click=State.set_filter("all"),
                    ),
                ),
                spacing="4",
            ),
            spacing="4",
            align_items="stretch",
            width="100%",
        ),
        _job_cards(),
        spacing="2",
        padding="2",
        align_items="stretch",
        width="80%",
        margin="0 auto",
    )
