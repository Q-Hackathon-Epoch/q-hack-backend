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

agent_responses = {
    'modules_response': None,
    'grades_response': None,
    'cv_summary': None,
    'student_skills': None,
}

def trigger_pipeline(self_description: str):

    modules_path = './uploaded_files/module_handbook.pdf'
    grades_path = './uploaded_files/grade_sheet.pdf'
    cv_path = './uploaded_files/student_cv.pdf'
    description_path = './uploaded_files/students-self-description.txt'


    modules_input = convert_to_text(modules_path)
    modules_response = agents.get_uni_modules(modules_input)
    agent_responses['modules_response'] = modules_response


    grades_input = convert_to_text(grades_path)
    grades_response = agents.get_student_grades(modules_response, grades_input)


    cv_input = convert_to_text(cv_path)
    cv_summary = agents.get_cv_summary(cv_input)
    agent_responses['cv_summary'] = cv_summary


    print(cv_summary)


    student_skills = agents.get_self_description(self_description)
    agent_responses['student_skills'] = student_skills
    print(student_skills)

    return agent_responses

# todo: cv pdf

    def compute_roadmap():
        pass
        