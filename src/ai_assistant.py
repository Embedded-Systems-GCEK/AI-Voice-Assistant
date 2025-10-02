"""
AI Assistant module that integrates various components such as speech recognition,
"""

# Import all AI Providers
from assistant.ai_provider.ai_providers import AIProvider
import assistant.ai_provider as ai
from assistant.assistant import ConversationalAssistant

class AIAssistant(ConversationalAssistant):
    def __init__(
        self,
        ai_provider: AIProvider = ai.Ollama(),
        name: str = "AI Assistant"
    ):
        super().__init__(
            ai_provider=ai_provider,
            name=name
        )

    def change_ai_provider(self, new_provider: AIProvider) -> None:
        self.ai_provider = new_provider
        print(f"🤖 AI Provider changed to {new_provider.name}")

    def ask(self, prompt: str):
        self.response = self.ai_provider.ask_with_timeout(prompt)
        self.answer(self.response)
        return self.response


class AISingleton:
    """Singleton class to manage the global AI Assistant instance"""
    _instance = None
    _assistant = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AISingleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_assistant(cls) -> AIAssistant:
        """Get the singleton AI assistant instance"""
        if cls._assistant is None:
            cls._assistant = AIAssistant()
        return cls._assistant

    @classmethod
    def initialize_assistant(cls, ai_provider: AIProvider = None, name: str = "AI Assistant") -> AIAssistant:
        """Initialize the singleton assistant with custom parameters"""
        if ai_provider is not None:
            cls._assistant = AIAssistant(ai_provider=ai_provider, name=name)
        else:
            cls._assistant = AIAssistant(name=name)
        return cls._assistant

    @classmethod
    def reset_assistant(cls):
        """Reset the assistant instance"""
        cls._assistant = None

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if assistant is initialized"""
        return cls._assistant is not None


# Global singleton instance
ai_singleton = AISingleton()

ai_singleton.initialize_assistant(name="Minix")


def get_ai_assistant() -> AIAssistant:
    """Convenience function to get the AI assistant singleton"""
    assistant = ai_singleton.get_assistant()
    print(f"Using AI Assistant: {assistant.name} , AI Provider: {assistant.ai_provider.name} ID {id(assistant)}")
    return assistant

def initialize_ai_assistant(ai_provider: AIProvider = None, name: str = "AI Assistant") -> AIAssistant:
    """Convenience function to initialize the AI assistant singleton"""
    return ai_singleton.initialize_assistant(ai_provider, name)

