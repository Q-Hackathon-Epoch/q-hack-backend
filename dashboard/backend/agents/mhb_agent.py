import logging
from datetime import datetime

from dashboard.backend.agents.agent import LLMAgent
from dashboard.backend.utils.convert_to_text import convert_to_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_use(file_path: str):
    if not file_path:
        logger.error("No file path provided")
        return None

    try:
        raw_text = convert_to_text(file_path)
        if not raw_text:
            logger.error(f"Failed to extract text from {file_path}")
            return None
    except Exception as e:
        logger.error(f"Text conversion failed: {str(e)}")
        return None

    current_date = datetime.now().strftime("%Y-%m-%d")

    system_prompt = f"""You are an expert academic assistant analyzing course syllabi. For the given course material:
    1. Extract ALL lecture information including:
       - Lecture titles/topics
       - Dates/times (convert to ISO format if needed)
       - Locations (physical or virtual)
       - Required readings/materials
       - Assignment deadlines
    
    2. For each lecture, identify:
       - Key learning objectives
       - Important concepts
       - Related assessments
    
    3. Format output as JSON with these keys:
       - "course_meta" (code, title, term)
       - "schedule" (chronological list)
       - "deadlines" (sorted by date)
       - "weekly_prep" (summary of weekly commitments)
    
    Current date: {current_date}
    Course context: {raw_text}"""

    try:
        agent = LLMAgent(
            system_prompt=system_prompt,
            azure_endpoint="",
            api_key="",
            api_version="2025-01-01-preview",
            model="your_deployment_name"
        )

        response = agent.call_llm
        return response

    except Exception as e:
        logger.error(f"LLM processing failed: {str(e)}")
        return None