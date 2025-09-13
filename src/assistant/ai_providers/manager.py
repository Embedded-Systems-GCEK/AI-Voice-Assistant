"""
AI Provider Manager
Manages multiple AI providers and handles fallback logic.
"""

from typing import Dict, List, Optional
from .base_provider import BaseAIProvider
from .gpt5_provider import GPT5Provider
from .ollama_provider import OllamaProvider
from .config import AIProvidersConfig


class AIProviderManager:
    """Manages multiple AI providers with fallback support."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the AI Provider Manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = AIProvidersConfig(config_file) if config_file else AIProvidersConfig()
        self.providers: Dict[str, BaseAIProvider] = {}
        self._initialize_providers()
    
    def _initialize_providers(self) -> None:
        """Initialize all configured providers."""
        # Initialize GPT-5 provider
        if self.config.is_provider_enabled("gpt5"):
            gpt5_config = self.config.get_gpt5_config()
            try:
                self.providers["gpt5"] = GPT5Provider(**gpt5_config)
                print(f"✅ GPT-5 provider initialized")
            except Exception as e:
                print(f"⚠️  Failed to initialize GPT-5 provider: {e}")
        
        # Initialize Ollama provider
        if self.config.is_provider_enabled("ollama"):
            ollama_config = self.config.get_ollama_config()
            try:
                self.providers["ollama"] = OllamaProvider(**ollama_config)
                print(f"✅ Ollama provider initialized")
            except Exception as e:
                print(f"⚠️  Failed to initialize Ollama provider: {e}")
    
    def get_provider(self, provider_name: str) -> Optional[BaseAIProvider]:
        """Get a specific provider by name."""
        return self.providers.get(provider_name)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names."""
        return [name for name, provider in self.providers.items() if provider.is_online()]
    
    def get_primary_provider(self) -> Optional[BaseAIProvider]:
        """Get the primary (preferred) available provider."""
        # Try default provider first
        default_provider = self.config.get_default_provider()
        if default_provider in self.providers and self.providers[default_provider].is_online():
            return self.providers[default_provider]
        
        # Fallback to any available provider
        for provider in self.providers.values():
            if provider.is_online():
                return provider
        
        return None
    
    def generate_response(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3, 
                         preferred_provider: Optional[str] = None) -> tuple[str, str]:
        """
        Generate response using the best available provider.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens in response
            temperature: Response randomness
            preferred_provider: Preferred provider name (optional)
            
        Returns:
            Tuple of (response, provider_name_used)
        """
        # Try preferred provider first
        if preferred_provider and preferred_provider in self.providers:
            provider = self.providers[preferred_provider]
            if provider.is_online():
                response = provider.generate_response(prompt, max_tokens, temperature)
                if not response.startswith("Error"):
                    return response, preferred_provider
        
        # Try primary provider
        primary_provider = self.get_primary_provider()
        if primary_provider:
            response = primary_provider.generate_response(prompt, max_tokens, temperature)
            if not response.startswith("Error"):
                return response, primary_provider.name
        
        # Try all available providers if fallback is enabled
        if self.config.is_fallback_enabled():
            for name, provider in self.providers.items():
                if provider.is_online():
                    response = provider.generate_response(prompt, max_tokens, temperature)
                    if not response.startswith("Error"):
                        return response, name
        
        return "Sorry, no AI providers are currently available.", "none"
    
    def get_providers_status(self) -> Dict[str, Dict]:
        """Get status of all providers."""
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                "available": provider.is_online(),
                "info": provider.get_provider_info()
            }
        return status
    
    def test_all_providers(self) -> Dict[str, bool]:
        """Test all providers and return their status."""
        results = {}
        for name, provider in self.providers.items():
            try:
                # Force re-test connection
                provider._test_connection()
                results[name] = provider.is_online()
            except Exception as e:
                print(f"Error testing {name}: {e}")
                results[name] = False
        return results
    
    def add_provider(self, name: str, provider: BaseAIProvider) -> None:
        """Add a custom provider."""
        self.providers[name] = provider
    
    def remove_provider(self, name: str) -> bool:
        """Remove a provider."""
        if name in self.providers:
            del self.providers[name]
            return True
        return False