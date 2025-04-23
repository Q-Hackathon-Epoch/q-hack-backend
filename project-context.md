# Project context:

A hackathon project where we are working on developing an application using Reflex library.
The app is focused towards students. Based on various inputs received by the student, different agents will analyse different aspects of the students inputs and create a profile. Then this profile will be used to help students:

1. Upskill for the goals they have described (e.g. further studies, dream job, or own startup) by creating a roadmap (recommended projects, events to attend, internships, etc.) for them to follow to improve their chances of achieving their goals.
2. Manage their studies better, by providing them with a roadmap of the University modules they should take in order to achieve their goals
3. Help them with job/internship search by recommending jobs/internships that are aligned with their goals, current skills and experience.

## Tech stack:

- Frontend: Reflex (Python web framework)
- Backend: Azure OpenAI service (for agent-based architecture), Azure Search (for RAG), langchain, langgraph, Agent based architecture

# User flow

## Input Screen (Screen 1)

Page heading says something along the lines of "Let's try to know you better". Then below that, there are 3 drag and drop boxes (1 - 3) and one text box (4):

1. Box 1. - Heading: "Please help me understand what your university currently offers. Hint: Module handbook". User uploads their University Module Handbook.
2. Box 2. - Heading: "Please tell me what which modules have you already passed. Hint: grade sheet". User uploads their current grade sheet.
3. Box 3. - Heading: "Please tell me about your skills and experience. Hint: CV or LinkedIn HTML". User uploads their CV or LinkedIn HTML.
4. Box 4. - Heading: "Please tell me about your strengths, weaknesses, goals and problems you are facing". User describes their strengths, weaknesses, goals (further studies, or dream job or own startup, or internship, or exhange semester, or working student job, or all of it) and problems they are facing in a text box.

This is presented in a friendly and engaging manner, with a progress bar at the top of the page to show the user how far they are in the process. The user can also see a preview of their uploaded files in the drag and drop boxes.

Finally there is a button at the bottom of the page that says "Let's go!" or something similar, which when clicked will take the user to the next screen.

## Behind the scenes processing

### File upload

When the user clicks the "Let's go!" button, the app will place/upload the files in local directory "uploaded_files". Further, the text input the user will be placed in a file called "students-self-description.txt".

The backend app will create files called "university-modules", "students-grade-sheet", "students-cv", "students-profile" and "recommended-jobs" in the same directory, which will be used to store various of the university module, student's profile and job related data information. These files can have the most suitable format and file type, optimised for the agentic processing that will be done on them. For example, the "university-modules" file can be a JSON file that contains the module handbook data in a structured format, which can be easily read and processed by the various agents. The "students-profile" file can also be a JSON file that contains the student's profile information in a structured format, which can be easily read and processed by the various agents.

### Agentic input processing (code in the backend directory)

Some mechanism should be developed, such that once the files are uploaded, the various relevant agents are triggered to do their analysis. Overall, by utilising multi-agentic orchestration facilitated by langchain and langgraph, the app should be able to process the uploaded files and the students-self-description.txt input to analyze the University module handbook data, the student data and put together a personalised student profile. This will involve the following agents:

- module_handbook_agent: This agent will read the module handbook and extract various information related to the modules that are available to the student, such as the module name, descriptions of each module, including the prerequisites and the skills that are required for each module, their credits, their workload, etc. All this analysed data will be stored in an appropriate format in the "university-modules", which will be used by the other agents to retrieve relevant information about what is even possible for the student to take.
- grade_sheet_agent: This agent will read the grade sheet and extract various information related to the modules that the student has already passed, such as the module name, grades, credits, etc. This agent will also be responsible for storing the grade sheet data in the "students-grade-sheet" file, which will be used by the other agents to retrieve relevant information about what modules the student has already completed.
- cv_agent: This agent will read the CV or LinkedIn HTML and extract various information related to the student's skills and experience, such as the skills they have, their work experience, projects they have worked on, etc. This agent will also be responsible for storing the CV data in the "students-cv" file, which will be used by the other agents to retrieve relevant information about the student's skills and experience.
- student_profile_agent: This agent will compile all the information gathered from the grade_sheet_agent, cv_agent and the file "students-self-description.txt" to create a comprehensive student profile and store it in a suitable format in the "students-profile" file.

### Agentic output processing

- uni_roadmap_agent: This agent will use the information gathered from the module_handbook_agent and student_profile_agent to create a personalized University roadmap for the student, which will include recommendations for modules to take in order to achieve their goals, a specific and uniform json format. This will be used in the UI to display the recommended modules to the student.nts-profile" file, which will be used by the other agents to retrieve relevant information about the student's University roadmap.
- job_recommendation_agent: This agent will have access to a hardcoded json of mock jobs data. This will then be used in conjunction with the information gathered from the student_profile_agent to recommend the specific jobs which are suitable for the students based on their profile, goals, strengths, etc. This information is then stored in "recommended-jobs" file for use by the next agent. On the UI side, the recommended jobs will be displayed as a list of recommended jobs for the student to apply for.
- upskill_roadmap_agent: This agent will use the information gathered from the student_profile_agent and the job_recommendation_agent to create a personalized upskilling roadmap for the student, which will include recommendations for projects, types of events/internships to attend, etc. in order to achieve their goals.

# Tasks to be completed:

- Create the UI for the input screen, including the drag and drop boxes, text box, progress bar, and button.
- Implement the file upload functionality to store the uploaded files in the "uploaded_files" directory and create the necessary files for agentic processing upon clicking the button.
- Implement the agentic processing functionality to analyze the uploaded files and create the student profile using the various agents.
- Develop the logic for the module_handbook_agent, grade_sheet_agent, cv_agent, and student_profile_agent to ensure they correctly process the respective inputs and generate the required outputs. For this, relevant tools must be created in the backend directory, which will be used by the agents to process various inputs and generate the required outputs.
- Implement the logic for the uni_roadmap_agent, job_recommendation_agent, and upskill_roadmap_agent to generate the personalized recommendations based on the student profile and other inputs.
- Feel free to improve the wordings of the headings to sound more natural and friendly wherever necessary.
