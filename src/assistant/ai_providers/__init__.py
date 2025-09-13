# AI Voice Assistant - AI Providers Module
"""
This module contains different AI provider implementations for the voice assistant.
Supported providers:
- GPT-5 (Azure OpenAI)
- Ollama (local inference)
"""

from .base_provider import BaseAIProvider
from .gpt5_provider import GPT5Provider
from .ollama_provider import OllamaProvider
from .manager import AIProviderManager
from .config import AIProvidersConfig

__all__ = [
    "BaseAIProvider", 
    "GPT5Provider", 
    "OllamaProvider", 
    "AIProviderManager", 
    "AIProvidersConfig"
]