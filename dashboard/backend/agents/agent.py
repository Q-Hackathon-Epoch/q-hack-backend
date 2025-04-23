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
