"""
Base AI Provider Interface
This defines the interface that all AI providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseAIProvider(ABC):
    """Abstract base class for all AI providers."""
    
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.is_available = False
        self._test_connection()
    
    @abstractmethod
    def _test_connection(self) -> bool:
        """Test if the AI provider is available and properly configured."""
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> str:
        """
        Generate a response from the AI provider.
        
        Args:
            prompt: The input prompt/question
            max_tokens: Maximum number of tokens in the response
            temperature: Response randomness (0.0 = deterministic, 1.0 = random)
            
        Returns:
            Generated response text
        """
        pass
    
    @abstractmethod
    def get_provider_info(self) -> dict:
        """Return information about this provider."""
        pass
    
    def is_online(self) -> bool:
        """Check if the provider is online and available."""
        return self.is_available