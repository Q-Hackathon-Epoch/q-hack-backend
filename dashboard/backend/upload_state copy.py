from dashboard.backend.utils.convert_to_text import convert_to_text

from langchain_openai.chat_models import AzureChatOpenAI
from dashboard.backend.agents.Agents import Agents

import reflex as rx
from dotenv import load_dotenv
import os
load_dotenv()


api_key = os.environ['AZURE_OPENAI_TOKEN']

llm_model = AzureChatOpenAI(model='gpt-4.1-mini-2',
                        api_key=os.environ['AZURE_OPENAI_TOKEN'],
                        api_version='2024-12-01-preview', 
                        azure_endpoint="https://subad-m9u2eiah-eastus2.cognitiveservices.azure.com/")
agents = Agents(llm_model)

class ProcessingState(rx.State):
    modules_path = ''
    grades_path = ''

    # def set_modules_path(self, path):
    #     self.modules_path = path
    #     self.current_modules_response()
    #     self.current_grades_response()

    # def set_grades_path(self, path):
    #     self.grades_path = path
    #     self.current_grades_response()

    @rx.var(cache=True)
    def current_modules_response(self) -> str:
    #def update_modules_response(self, path):
        #self.modules_path = path
        print('calling llm')
        if self.modules_path == '':
            return ''
        modules_input = convert_to_text(self.modules_path)
        result = agents.get_uni_modules(modules_input)
        print(result)

        # if self.grades_path != '':
        #     self
        return result

    @rx.var(cache=True)
    def current_grades_response(self) -> str:
    #def update_grades_response(self, path):
        #self.grades_path = path
        print('calling llm')
        if self.grades_path == '' or self.modules_path == '':
            return ''
        grades_input = convert_to_text(self.grades_path)
        result = agents.get_student_grades(self.current_modules_response, grades_input)
        print(result)
        return result

# todo: cv pdf

    def compute_roadmap():
        pass
        