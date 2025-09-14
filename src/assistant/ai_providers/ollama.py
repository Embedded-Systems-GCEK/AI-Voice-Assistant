import subprocess
import requests

# custom import
try:
    from .ai_providers import AIProvider, AiProviderList, AiProviderStatus
except ImportError:
    from ai_providers import AIProvider, AiProviderList, AiProviderStatus
    
class Ollama(AIProvider):
    def __init__(self):
        super().__init__()
        self.model: str = "tinyllama"
        # Override base class defaults for Ollama
        self.temperature = 0

    @property
    def name(self) -> str:
        return AiProviderList.OLLAMA.value
    
    def _call_api(self, message: list[dict[str, str]] | str) -> str:
        """Implementation of the abstract _call_api method for Ollama"""
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
                        "temperature": self.temperature
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

    def ask_ollama_api(self, message: list[dict[str, str]] | str) -> str:
        """Legacy method - now delegates to _call_api"""
        return self._call_api(message)
    
    def ask(self, prompt: str) -> str:
        """Use the generic ask implementation from base class"""
        # Call parent ask method to handle message logging and stop checks
        super().ask(prompt)
        # Use generic ask for the actual API call
        return self._generic_ask(prompt)

if __name__ == "__main__":
    
    print(f"🤖 Testing {str(Ollama.name).capitalize()} with Memory/Context")
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
        print(f"⏳ Response Time {i}: {ollama.response_time:.2f} seconds")

    print("\n" + "=" * 50)
    print("📚 FULL CONVERSATION HISTORY:")
    ollama.show_conversation_history()

    print("\n📊 CONVERSATION STATISTICS:")
    stats = ollama.get_conversation_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\n🧹 Clearing conversation history...")
    print()
    for obj in ollama.QandAs:
        print(obj.to_dict())
    
    ollama.clear_messages()
    ollama.show_conversation_history()