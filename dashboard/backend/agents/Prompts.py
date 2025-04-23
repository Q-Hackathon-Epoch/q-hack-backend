system_lecture = """
You are an expert academic assistant analyzing course syllabi. For the given course material:

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
Course context: {course_code}"""

user_lecture = """Please analyze this course material:

{modules_text}

Return comprehensive, structured information as specified in the system prompt."""
# Highlight any time-sensitive items based on current date {current_date}."""

#schema_lecture = {
#    "courses": {



system_grades = """
You are an expert academic assistant analyzing student grades.
You have access to a description of the course and the grades of the student.

transform the grades into a structured format, showing skills the student has acquired and the skills they need to improve.
Also provide a summary that an employer can understand."""
#Based on the queries create a summary skill map for the student.
#"""

# todo: provide query tool for lectures
user_grades = """
Here are the lecture descriptions:
{lectures_mapping}
Please analyze the grades and extract skill gaps and areas for improvement:
{grades_text}
"""

system_jobs = """
You are an expert academic assistant analyzing job postings.
You have access to the following tool to query information about job postings

You have to find good matching jobs for the student.
"""
user_jobs = """
Please analyze job postings and extract relevant information, this is my skill set:
{skills}
"""

roadmap = ""