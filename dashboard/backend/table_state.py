import csv
from pathlib import Path
from typing import List
from dashboard.backend.utils.convert_to_text import convert_to_text

from langchain_openai.chat_models import AzureChatOpenAI
from dashboard.backend.agents.Agents import Agents

import reflex as rx
from dotenv import load_dotenv
import os
load_dotenv()

class Item(rx.Base):
    """The item class."""

    name: str
    payment: float
    date: str
    status: str
api_key = os.environ['AZURE_OPENAI_TOKEN']

llm_model = AzureChatOpenAI(model='gpt-4.1-mini-2',
                        api_key=os.environ['AZURE_OPENAI_TOKEN'],
                        api_version='2024-12-01-preview', 
                        azure_endpoint="https://subad-m9u2eiah-eastus2.cognitiveservices.azure.com/")
agents = Agents(llm_model)
class ProcessingState(rx.State):
    modules_path = ''
    grades_path = ''

    @rx.var(cache=True)
    def current_modules_response(self) -> str:
        if self.modules_path == '':
            return ''
        modules_input = convert_to_text(self.modules_path)
        result = agents.get_uni_modules(modules_input)
        #print(result)
        return result

    @rx.var(cache=True)
    def current_grades_response(self) -> str:
        if self.grades_path == '' or self.modules_path == '':
            return ''
        grades_input = convert_to_text(self.grades_path)
        result = agents.get_student_grades(self.current_modules_response, grades_input)
        print(result)
        return result

# todo: cv pdf

    def compute_roadmap():
        pass
        

class TableState(rx.State):
    """The state class."""

    items: List[Item] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Item]:
        items = self.items

        # Filter items based on selected item
        if self.sort_value:
            if self.sort_value in ["payment"]:
                items = sorted(
                    items,
                    key=lambda item: float(getattr(item, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                items = sorted(
                    items,
                    key=lambda item: str(getattr(item, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in [
                        "name",
                        "payment",
                        "date",
                        "status",
                    ]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 1
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Item]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        with Path("items.csv").open(mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.items = [Item(**row) for row in reader]
            self.total_items = len(self.items)

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()
