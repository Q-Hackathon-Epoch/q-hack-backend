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


def trigger_pipeline():

    modules_path = './uploaded_files/module_handbook.pdf'
    grades_path = './uploaded_files/grade_sheet.pdf'

    #print('calling llm')

    modules_input = convert_to_text(modules_path)
    modules_response = agents.get_uni_modules(modules_input)
    #print(result)

    #print('calling llm')
    grades_input = convert_to_text(grades_path)
    grades_response = agents.get_student_grades(modules_response, grades_input)
    #print(result)


    return None

# todo: cv pdf

    def compute_roadmap():
        pass
        