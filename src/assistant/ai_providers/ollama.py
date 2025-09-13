import subprocess

import requests
from sqlalchemy import false

# custom import

from ai_providers import AiProvider, AiProviderList, AiProviderStatus
class Ollama(AiProvider):
    def __init__(self):
        super().__init__()
        self.model: str = "tinyllama"

    @property
    def name(self) -> str:
        return AiProviderList.OLLAMA.value
    

    def ask_ollama_api(self, message: list[dict[str, str]] | str) -> str:
        try:
            # Prepare messages for Ollama API
            if isinstance(message, str):
                # Single message
                ollama_messages = [{"role": "user", "content": message}]
            else:
                # Full conversation history - send all messages for context
                ollama_messages = message.copy()

            response = requests.post(
                "http://localhost:11434/api/chat/",
                json={
                    "model": self.model,
                    "messages": ollama_messages,  # Send full conversation history
                    "stream": False,
                    "options": {
                        "temperature": 0
                    }
                },
            )
            response.raise_for_status()
            data = response.json()

            # Add assistant's response to conversation history
            assistant_response = data['message']['content']
            if isinstance(message, list):
                self.add_message("assistant", assistant_response)

            return assistant_response

        except requests.RequestException as e:
            self.status = AiProviderStatus.ERROR
            return f"Error communicating with Ollama API: {e}"
    
    def ask(self, prompt: str) -> str:
        try:
            self.status = AiProviderStatus.BUSY
            self.add_message("user", prompt)
            # Send full conversation history for context
            self.answer = self.ask_ollama_api(self.messages)
            self.status = AiProviderStatus.IDLE
            return self.answer
        except Exception as e:
            self.status = AiProviderStatus.ERROR
            return f"Error communicating with Ollama: {e}"

if __name__ == "__main__":
    print("🤖 Testing Ollama with Memory/Context")
    print("=" * 50)

    questions = [
        "Hello! My name is Arun CS",
        "What's my name?",
    ]

    ollama = Ollama()

    for i, q in enumerate(questions, 1):
        print(f"\n🐸 Arun > {q}")
        answer = ollama.ask(q)
        print(f"🤖 Ollama > {answer}")
        print(f"⏳ Response Time {i}: {ollama.get_response_time():.2f} seconds")

    print("\n" + "=" * 50)
    print("📚 FULL CONVERSATION HISTORY:")
    ollama.show_conversation_history()

    print("\n📊 CONVERSATION STATISTICS:")
    stats = ollama.get_conversation_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\n🧹 Clearing conversation history...")
    ollama.clear_messages()
    ollama.show_conversation_history()