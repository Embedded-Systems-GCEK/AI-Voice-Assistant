import os
import requests
from typing import Optional

# Custom Imports
try:
    from .ai_providers import AIProvider, AiProviderList, AiProviderStatus
except ImportError:
    from ai_providers import AIProvider, AiProviderList, AiProviderStatus

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class Llama(AIProvider):
    def __init__(self, token: Optional[str] = GITHUB_TOKEN):
        super().__init__()
        if not token:
            raise ValueError("GITHUB_TOKEN not found.")
        self.token = token
        self.model = "meta/Llama-4-Scout-17B-16E-Instruct"
        self.url = "https://models.github.ai/inference/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-GitHub-Api-Version": "2023-11-28"
        }
        self.add_message("system", "You are a helpful AI voice/text assistant")

    @property
    def name(self) -> str:
        return "GitHub Llama"

    def _call_api(self, message: list[dict[str, str]] | str) -> str:
        """Implementation of the abstract _call_api method for GitHub Llama"""
        try:
            payload = {
                "model": self.model,
                "messages": message if isinstance(message, list) else [{"role": "user", "content": message}],
                "max_tokens": self._max_tokens,
                "temperature": self._temperature
            }

            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()

            assistant_response = data["choices"][0]["message"]["content"]
            
            if isinstance(message, list):
                self.add_message("assistant", assistant_response)

            return assistant_response

        except requests.RequestException as e:
            self.status = AiProviderStatus.ERROR
            return f"Error communicating with GitHub Llama API: {e}"
        except KeyError as e:
            self.status = AiProviderStatus.ERROR
            return f"Unexpected response format from GitHub Llama API: {e}"

    def ask(self, prompt: str) -> str:
        """Use the generic ask implementation from base class"""
        super().ask(prompt)
        return self._generic_ask(prompt)

    def ask_llama_api(self, message: list[dict[str, str]] | str) -> str:
        """Legacy method - now delegates to _call_api"""
        return self._call_api(message)


if __name__ == "__main__":
    print("🤖 Testing GitHub Llama with Memory/Context")
    print("=" * 50)

    questions = [
        "Hello! My name is Arun CS",
        "What's my name?",
    ]

    llama = Llama()

    for i, q in enumerate(questions, 1):
        print(f"\n🐸 Arun > {q}")
        answer = llama.ask(q)
        print(f"🤖 Llama > {answer}")
        print(f"⏳ Response Time {i}: {llama.response_time:.2f} seconds")

    print("\n" + "=" * 50)
    print("📚 FULL CONVERSATION HISTORY:")
    llama.show_conversation_history()

    print("\n📊 CONVERSATION STATISTICS:")
    stats = llama.get_conversation_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
