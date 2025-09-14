import cohere

COHERE_API_KEY = ""

# Custom Imports
try:
    from .ai_providers import AIProvider, AiProviderList, AiProviderStatus
except ImportError:
    from ai_providers import AIProvider, AiProviderList, AiProviderStatus

class CohereAPI(AIProvider):
    def __init__(self, api_key: str = COHERE_API_KEY):
        super().__init__()
        self.client = cohere.Client(api_key)
        # Use base class defaults or override as needed
        # self.temperature = 0.3  # already set in base class
        # self.max_tokens = 150   # already set in base class

    @property
    def name(self) -> str:
        return AiProviderList.COHERE.value

    def _call_api(self, message: list[dict[str, str]] | str) -> str:
        """Implementation of the abstract _call_api method for Cohere"""
        try:
            # Prepare message for Cohere API
            if isinstance(message, str):
                # Single message
                chat_message = message
            else:
                # Full conversation history - format for Cohere
                # Cohere's chat API expects a single message string, so we'll format the conversation
                formatted_messages = []
                for msg in message:
                    role = "Human" if msg['role'] == 'user' else "Assistant"
                    formatted_messages.append(f"{role}: {msg['content']}")
                chat_message = "\n".join(formatted_messages)

            response = self.client.chat(
                message=chat_message,
                temperature=self._temperature,
                max_tokens=self._max_tokens
            )

            # Extract assistant's response
            assistant_response = response.text.strip()
            if isinstance(message, list):
                self.add_message("assistant", assistant_response)

            return assistant_response

        except Exception as e:
            self.status = AiProviderStatus.ERROR
            return f"Error communicating with Cohere API: {e}"

    def ask_cohere_api(self, message: list[dict[str, str]] | str) -> str:
        """Legacy method - now delegates to _call_api"""
        return self._call_api(message)

    def ask(self, prompt: str) -> str:
        """Use the generic ask implementation from base class"""
        super().ask(prompt)
        return self._generic_ask(prompt)

if __name__ == "__main__":
    print("🤖 Testing Cohere with Memory/Context")
    print("=" * 50)

    questions = [
        "Hello! My name is Arun CS",
        "What's my name?",
    ]

    cohere_api = CohereAPI()

    for i, q in enumerate(questions, 1):
        print(f"\n🐸 Arun > {q}")
        answer = cohere_api.ask(q)
        print(f"🤖 Cohere > {answer}")
        print(f"⏳ Response Time {i}: {cohere_api.response_time:.2f} seconds")

    print("\n" + "=" * 50)
    print("📚 FULL CONVERSATION HISTORY:")
    cohere_api.show_conversation_history()

    print("\n📊 CONVERSATION STATISTICS:")
    stats = cohere_api.get_conversation_stats()
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\n🧹 Clearing conversation history...")
    print()
    for obj in cohere_api.QandAs:
        print(obj.to_dict())
    
    cohere_api.clear_messages()
    cohere_api.show_conversation_history()