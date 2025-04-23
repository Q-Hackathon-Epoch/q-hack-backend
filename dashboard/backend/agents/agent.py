from azure.ai.openai import AzureOpenAI
from config.settings import endpoint, subscription_key, deployment


class LLMAgent:
    def __init__(self, system_prompt: str, azure_endpoint: str, api_key: str, api_version: str, model: str):
        # Create a dedicated Azure OpenAI client for this agent
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.model = model
        self.system_prompt = system_prompt
        self.chat_prompt = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]}
        ]

    def call_llm(self, user_input: str) -> str:
        messages = self.chat_prompt.copy()
        messages.append({"role": "user", "content": [{"type": "text", "text": user_input}]})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_completion_tokens=1000,
            stop=None,
            stream=False
        )
        return completion.choices[0].message.content


skill_compare_agent = LLMAgent(
    system_prompt="Compare user skills to target role skills and identify gaps. Format as: 'Missing Skills: [...]' and 'Matching Skills: [...]'.",
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    model=deployment
)


roadmap_agent = LLMAgent(
    system_prompt="Generate a learning roadmap with suggestions, project ideas, and resource links based on skill gaps.",
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    model=deployment
)


interview_agent = LLMAgent(
    system_prompt="Generate interview preparation questions based on skill gaps and the target role.",
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    model=deployment
)


resume_agent = LLMAgent(
    system_prompt="Generate a sample resume bullet point highlighting a skill or experience relevant to the target role.",
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    model=der
    model=deployment
)