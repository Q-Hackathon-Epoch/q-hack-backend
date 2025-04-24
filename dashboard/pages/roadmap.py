import reflex as rx
from ..templates import template
from ..backend.upload_state import agent_responses
import asyncio

class State(rx.State):
    completed_ids: list[int] = []
    roadmap_steps: list[dict] = []

    def toggle_step(self, step_id: int):
        if step_id in self.completed_ids:
            self.completed_ids.remove(step_id)
        else:
            self.completed_ids.append(step_id)

    @rx.var
    def total_xp(self) -> int:
        return len(self.completed_ids) * 20

    @rx.event(background=True)
    async def poll_roadmap(self):
        while True:
            # Получаем «сырые» шаги – это может быть list[str] или list[dict]
            raw = agent_responses.get("roadmap_response", []) or []
            normalized: list[dict] = []
            for idx, item in enumerate(raw):
                if isinstance(item, dict):
                    # Если уже dict, убеждаемся, что есть id и description
                    normalized.append({
                        "id": item.get("id", idx),
                        "description": item.get("description", str(item))
                    })
                else:
                    # Если строка, упаковываем её
                    normalized.append({
                        "id": idx,
                        "description": str(item)
                    })
            # Присваиваем только если есть изменения
            if normalized != self.roadmap_steps:
                async with self:
                    self.roadmap_steps = normalized
            await asyncio.sleep(1)

def _task_list() -> rx.Component:
    return rx.vstack(
        rx.foreach(
            State.roadmap_steps,
            lambda step: rx.hstack(
                rx.checkbox(
                    # is_checked — Var[bool], всё ок
                    is_checked=State.completed_ids.contains(step["id"]),
                    # Первый аргумент — булево значение, его игнорируем (_)
                    # А нужный нам step передаём через дефолт step=step
                    on_change=lambda _, step=step: State.toggle_step(step["id"]),
                ),
                rx.text(step["description"], font_size="md"),
                spacing="2",
                align_items="center",
            ),
        ),
        spacing="3",
        width="100%",
    )

@template(route="/roadmap", title="Your Roadmap", on_load=[State.poll_roadmap])
@rx.page()
def Roadmap() -> rx.Component:
    return rx.vstack(
        rx.heading("To-Do List", size="9", margin_bottom="1rem"),
        _task_list(),
        rx.divider(margin_top="1.5rem"),
        rx.hstack(
            rx.text("Total XP:", font_size="lg", font_weight="semibold"),
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
