from dashboard.backend.agents.agent import LLMAgent
from dashboard.backend.utils.convert_to_text import convert_to_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_use(file_path: str, course_code: Optional[str] = None) -> Optional[Dict[str, List[str]]]:
    """
    Process a course syllabus (PDF/HTML) and extract structured lecture information.

    Args:
        file_path: Path to the syllabus file (PDF or HTML)
        course_code: Optional course code for context

    Returns:
        Dict with keys: 'summary', 'schedule', 'deadlines'
        None if processing fails
    """
    # Validate input
    if not file_path:
        logger.error("No file path provided")
        return None

    # Step 1: Convert document to text
    try:
        raw_text = convert_to_text(file_path)
        if not raw_text:
            logger.error(f"Failed to extract text from {file_path}")
            return None
    except Exception as e:
        logger.error(f"Text conversion failed: {str(e)}")
        return None

    # Step 2: Prepare optimized prompts
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
Course context: {course_code or 'Not specified'}"""

    user_prompt = f"""Please analyze this course material:

{raw_text[:20000]}  # Truncate to avoid token limits

Return comprehensive, structured information as specified in the system prompt.
Highlight any time-sensitive items based on current date {current_date}."""

    # Step 3: Initialize and query LLM
    try:
        agent = LLMAgent(
            system_prompt=system_prompt,
            azure_endpoint="your_azure_endpoint",  # Replace with actual
            api_key="your_api_key",  # Replace with actual
            api_version="2025-01-01-preview",
            model="your_deployment_name",  # Replace with actual
            temperature=0.3,  # More deterministic output
            max_tokens=4000
        )

        response = agent.generate_response(user_prompt)
        return _validate_and_parse_response(response)

    except Exception as e:
        logger.error(f"LLM processing failed: {str(e)}")
        return None


def _validate_and_parse_response(response: str) -> Optional[Dict]:
    """Validate and clean the LLM response"""
    try:
        # Basic validation
        if not response or len(response) < 20:
            logger.warning("Empty or insufficient LLM response")
            return None

        # Here you would add JSON parsing logic
        # For now returning raw response
        return {"raw_response": response}
    except Exception as e:
        logger.error(f"Response parsing failed: {str(e)}")
        return None