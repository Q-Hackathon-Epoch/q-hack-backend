import json
from pathlib import Path
import reflex as rx

from ..templates import template
from ..backend.upload_state import agent_responses


class State(rx.State):
    """Stores completed task IDs and computes total XP."""

    # Список ID выполненных шагов
    completed_ids: list[int] = []

    def toggle_step(self, step_id: int):
        """Добавляет или удаляет шаг из выполненных."""
        if step_id in self.completed_ids:
            self.completed_ids.remove(step_id)
        else:
            self.completed_ids.append(step_id)

    @rx.var
    def total_xp(self) -> int:
        """Общее количество XP на основе количества выполненных шагов."""
        return len(self.completed_ids) * 20


# Путь к JSON с данными шагов
# DATA_PATH = (
#     Path(__file__).resolve().parent.parent / "test_data" / "steps.json"
# )

# DATA_PATH = (
#     Path(__file__).resolve().parent.parent / "test_data" / "roadmap.json"
# )


def _load_steps() -> list[dict]:
    """Загружает список шагов из JSON и нормализует для отображения."""
    steps = agent_responses["roadmap_response"]
    normalized = []
    for step in steps:
        # Каждый шаг — это просто строка описания или объект с полями
        if isinstance(step, dict):
            desc = step.get("description", "")
            id_ = step.get("id")
        else:
            desc = str(step)
            id_ = len(normalized)
        normalized.append({
            "id": id_,
            "description": desc,
        })
    return normalized


def _task_list() -> rx.Component:
    """Возвращает vstack со списком шагов и чекбоксами."""
    steps = _load_steps()
    items = []
    for step in steps:
        is_done = State.completed_ids.contains(step["id"])
        items.append(
            rx.hstack(
                rx.checkbox(
                    is_checked=is_done,
                    on_change=State.toggle_step(step["id"]),
                ),
                rx.text(step["description"], font_size="md"),
                spacing="2",
                align_items="center",
            )
        )
    return rx.vstack(
        *items,
        spacing="3",
        width="100%",
    )


@template(route="/roadmap", title="Your Roadmap")
def Roadmap() -> rx.Component:
    """Страница со списком шагов и общим счётом XP."""
    return rx.vstack(
        rx.heading("To-Do List", size="9", margin_bottom="1rem"),
        _task_list(),
        rx.divider(margin_top="1.5rem"),
        rx.hstack(
            rx.text("Total XP:", font_size="lg", font_weight="semibold"),
            # Отображаем количество XP как State.total_xp var и добавляем приставку
            rx.text(State.total_xp, " XP", font_size="lg"),
            spacing="1",
            margin_top="1rem",
        ),
        spacing="2",
        padding="4",
        width="80%",
        mx="auto",
        align_items="flex-start",
    )