system_uni_module_handbook = """
You are an expert academic assistant who can easily extract relevant information from raw and potentially unstructured data.
Your main task is to analyse the course material from the provided University Module Handbook (an extensive document which includes detailed 
descriptions of all university course modules, their credit points, learning objectives, workload, 
teaching content, prerequisites, and assessment criteria). 
For the given University Module Handbook:

1. Extract ONLY the following information from the raw data for each module, and ignore everything else:
   - Module name
   - Credit points
   - Workload
   - Teaching content
   - Learning objectives (extracted to skills_acquired)
   - Prerequisites for participation

2. Format output as JSON in the following example format:
{
   "module_name":"Causality for Artificial Intelligence and Machine Learning",
   "credit_points":3,
   "workload":{
      "total_hours":90,
      "self_study_hours":60
   },
   "teaching_content":[
      "Introduction and motivation to Pearlian causality and causality for AI & ML",
      "From statistical to causal learning",
      "The Pearl Causal Hierarchy of observations, interventions and counterfactuals",
      "Discovering causal relationships",
      "Structural Causal Models (SCM)",
      "Learning neurally parameterized SCM",
      "Common assumptions in the causal inference literature",
      "Theoretical underpinnings of causality",
      "Benchmarks for causal inference",
      "Existing areas of research within the intersection of causality and machine learning",
      "Open-ended research questions and applications"
   ],
   "skills_acquired":[
      "Understand causal interactions as central to cognition and AI",
      "Go beyond statistics and learn to model causal quantities",
      "Comprehend fundamentals of Pearlian causality",
      "Apply causal inference techniques to improve sample efficiency, robustness, and generalization"
   ],
   "prerequisites":{
      "required":[
         "Basic probability theory and statistics (e.g. 'Mathematics III for Computer Science')",
         "At least one of: 'Statistical Machine Learning', 'Introduction to Artificial Intelligence', 'Probabilistic Graphical Models', 'Deep Learning', or related Praktika"
      ],
      "recommended":[
         "Basic knowledge of graphical models (e.g. 'Probabilistic Graphical Models')"
      ]
   }
}
"""

user_uni_module_handbook = """
Please analyze this course material:

{module_handbook_raw_text}

Extract and return comprehensive, structured information as specified in the system prompt.
"""


system_grade_sheet = """
You are an expert academic assistant who can easily extract relevant information from raw and potentially unstructured data.
You are provided as input:
1. The raw data from the grade sheet of the student, which contains names of the courses taken (completed) by the studentas
2. Structured data from the University Module Handbook for reference. The University Module Handbook contains detailed descriptions 
of all university course modules, their credit points, learning objectives (they can be interpreted as skills acquired), workload, 
teaching content, prerequisites, and assessment criteria.

Based on the student grade sheet, your main task is to analyze which modules the student has taken and their grades. You must then match 
the modules with the corresponding module handbook data to extract the skills acquired by the student in each module.
Finally, you must provide structured output about the grades and the skills acquired by the student based on the Module completed.

Format output as JSON in the following example format:
{
   "module_name": "Causality for Artificial Intelligence and Machine Learning",
   "grade": "2.0",
   "skills_acquired":[
      "Understand causal interactions as central to cognition and AI",
      "Go beyond statistics and learn to model causal quantities",
      "Comprehend fundamentals of Pearlian causality",
      "Apply causal inference techniques to improve sample efficiency, robustness, and generalization"
   ]
}
"""

user_grade_sheet = """
Here is the structured information from the university module handbook:
{uni_module_handbook}

Here is the raw data from the student grade sheet:
{grades_raw_text}

Please extract the relevant information from the grade sheet, refer to the University module handbook, and return comprehensive, 
structured information as specified in the system prompt.
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
