from dashboard.backend.utils.convert_to_text import convert_to_text

from langchain_openai.chat_models import AzureChatOpenAI
from dashboard.backend.agents.Agents import Agents
# from ..pages.jobs import State as jobState

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
    'job_offers_response': [],
    'roadmap_response': [],
}

def trigger_pipeline():

    modules_path = './uploaded_files/module_handbook.pdf'
    grades_path = './uploaded_files/grade_sheet.pdf'
    cv_path = './uploaded_files/student_cv.pdf'
    description_path = './uploaded_files/students-self-description.txt'
    job_offers_path = './dashboard/test_data/jobs.json'


    modules_input = convert_to_text(modules_path)
    modules_response = agents.get_uni_modules(modules_input)
    agent_responses['modules_response'] = modules_response


    grades_input = convert_to_text(grades_path)
    grades_response = agents.get_student_grades(modules_response, grades_input)
    agent_responses['grades_response'] = grades_response


    cv_input = convert_to_text(cv_path)
    cv_summary = agents.get_cv_summary(cv_input)
    agent_responses['cv_summary'] = cv_summary

    print(cv_summary)

    with open(description_path, 'r') as file:
        self_description = file.read()
    student_skills = agents.get_self_description(self_description)
    agent_responses['student_skills'] = student_skills
    print(student_skills)

    with open(job_offers_path, 'r') as file:
        job_offers = file.read()
    job_offers_response = agents.get_personalized_jobs(cv_summary, grades_response, student_skills, job_offers)
    agent_responses['job_offers_response'] = job_offers_response
    # jobState.matched_ids = job_offers_response
    print(job_offers_response)

    roadmap_response = agents.get_upskill_roadmap(modules_response, grades_response, cv_summary, student_skills)
    agent_responses['roadmap_response'] = roadmap_response
    print(roadmap_response)

    return agent_responses
        