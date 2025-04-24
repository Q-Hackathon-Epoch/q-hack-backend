from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI

from dashboard.backend.agents import Prompts

from dashboard.backend.utils.convert_to_text import convert_to_text

basic_schema = {
    "name": "llm_response",
    "schema": {
        "type": "object",
        "properties": {
            "answer": {"type": "string", "description": "The final json."},
        },
        "required": [
            "answer",
        ],
        "additionalProperties": False,
    },
    "strict": True,
}


def get_chat_prompt_template(system, user):
    return ChatPromptTemplate.from_messages(
        [("system", system), ("human", user)]
    )


class Agents:
    def __init__(self, llm_model: BaseChatModel):
        self.llm = llm_model

    def get_uni_modules(self, modules_text: str):
        prompt_template = get_chat_prompt_template(
            Prompts.system_uni_module_handbook,
            Prompts.user_uni_module_handbook,
        )
        chain = prompt_template | self.llm | StrOutputParser()
        # raw_text = convert_to_text(file_path)
        result = chain.invoke(
            {
                "module_handbook_raw_text": modules_text,
            }
        )
        return result

    def get_student_grades(self, uni_module_handbook: str, grades_raw_text: str):
        prompt_template = get_chat_prompt_template(
            Prompts.system_grade_sheet, Prompts.user_grade_sheet
        )
        chain = prompt_template | self.llm | StrOutputParser()
        result = chain.invoke(
            {
                "uni_module_handbook": uni_module_handbook,
                "grades_raw_text": grades_raw_text,
            }
        )
        return result
    
    def get_cv_summary(self, cv_raw_text: str):
        prompt_template = get_chat_prompt_template(
            Prompts.system_cv, Prompts.user_cv
        )
        chain = prompt_template | self.llm | StrOutputParser()
        result = chain.invoke(
            {
                "cv_raw_text": cv_raw_text,
            }
        )
        return result

    def get_self_description(self, questionnaire_raw_text: str):
        prompt_template = get_chat_prompt_template(
            Prompts.system_self_description, Prompts.user_self_description
        )
        chain = prompt_template | self.llm | StrOutputParser()
        result = chain.invoke(
            {
                "questionnaire_raw_text": questionnaire_raw_text,
            }
        )
        return result
    

    # output agents
    def get_personalized_jobs(self, cv_json, grade_sheet_json, self_description_json, job_postings_json):
        prompt_template = get_chat_prompt_template(
            Prompts.system_jobs_finder, Prompts.user_jobs_finder
        )
        chain = prompt_template | self.llm | StrOutputParser()
        result = chain.invoke(
            {
                "cv_json": cv_json,
                "grade_sheet_json": grade_sheet_json,
                "self_description_json": self_description_json,
                "job_postings_json": job_postings_json,
            }
        )
        return result


    def get_upskill_roadmap(self, uni_module_handbook_json, grade_sheet_json, cv_json, self_description_json):
        prompt_template = get_chat_prompt_template(
            Prompts.system_self_description, Prompts.user_self_description
        )
        chain = prompt_template | self.llm | StrOutputParser()
        result = chain.invoke(
            {
                "uni_module_handbook_json": uni_module_handbook_json,
                "grade_sheet_json": grade_sheet_json,
                "cv_json": cv_json,
                "self_description_json": self_description_json,
            }
        )
        return result