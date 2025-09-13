from .ollama import AiProvider
class Alexa(AiProvider):
    def __init__(self):
        pass
    
    def ask(self, prompt) -> str:
        # Placeholder implementation for Alexa
        return "Alexa response to: " + prompt
