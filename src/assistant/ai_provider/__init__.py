from .ai_providers import AIProvider # Import the base class
from .ollama import Ollama
from .github_gpt_5 import GPT_5
from .gemini import Gemini
from .llama import Llama
from .cohere_api import CohereAPI


__version__ = "0.1.0"

__all__ = ["AIProvider", "Ollama", "GPT_5", "Gemini", "Llama", "CohereAPI"]