import dotenv
from pathlib import Path
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Custom Import
from .ai_providers import AiProvider, AiProviderList, AiProviderStatus

from dotenv import load_dotenv
load_dotenv()


token = os.getenv('GITHUB_GPT_5_TOKEN', 'Hi')

class GPT_5(AiProvider):
    def __init__(self):
        super().__init__()
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-5"
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(token),
        )
    @property
    def name(self) -> str:
        return AiProviderList.GITHUB_GPT_5.value
    def get_answer(self,message):
        response = self.client.complete(
            messages=[
                # SystemMessage("You are a helpful assistant."),
                # UserMessage("What is the capital of France?"),
                # UserMessage("What is 2 + 2?"),
                UserMessage(message),
            ],
            model=self.model
        )
        answer = response.choices[0].message.content
        return answer
    def ask(self, prompt: str) -> str:
        if token is None:
            raise ValueError("GITHUB_GPT_5_TOKEN environment variable not set")
        self.status = AiProviderStatus.BUSY
        try:
            self.add_message("user", prompt)
            answer = self.get_answer(prompt)
            self.add_message("assistant", answer)
            self.answer = answer
            self.status = AiProviderStatus.IDLE
            return answer
        except Exception as e:
            self.status = AiProviderStatus.ERROR
            self.answer = f"Error: {str(e)}"
            return self.answer


if __name__ == "__main__":
    gpt_5 = GPT_5()
    print(gpt_5.ask("Remember my name is Arun CS"))
    print(gpt_5.ask("What is my name?"))



