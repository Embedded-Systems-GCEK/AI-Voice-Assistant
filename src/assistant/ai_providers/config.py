"""
AI Providers Configuration
Manages configuration and API keys for different AI providers.
"""

import os
import json
from typing import Dict, Any, Optional


class AIProvidersConfig:
    """Configuration manager for AI providers."""
    
    def __init__(self, config_file: str = "ai_providers_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
                return self._get_default_config()
        else:
            config = self._get_default_config()
            self._save_config(config)
            return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "gpt5": {
                "api_key": os.getenv("AZURE_OPENAI_API_KEY", "your-azure-openai-api-key-here"),
                "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-azure-openai-resource.openai.azure.com/"),
                "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5"),
                "api_version": "2024-02-15-preview",
                "enabled": True
            },
            "ollama": {
                "model": os.getenv("OLLAMA_MODEL", "mistral:7b"),
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                "use_api": True,
                "enabled": True
            },
            "default_provider": "ollama",  # Fallback to local provider
            "fallback_enabled": True
        }
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config file {self.config_file}: {e}")
    
    def get_gpt5_config(self) -> Dict[str, Any]:
        """Get GPT-5 configuration."""
        return self.config.get("gpt5", {})
    
    def get_ollama_config(self) -> Dict[str, Any]:
        """Get Ollama configuration."""
        return self.config.get("ollama", {})
    
    def set_gpt5_credentials(self, api_key: str, endpoint: str, deployment_name: Optional[str] = None) -> None:
        """Set GPT-5 credentials."""
        self.config.setdefault("gpt5", {})
        self.config["gpt5"]["api_key"] = api_key
        self.config["gpt5"]["endpoint"] = endpoint
        if deployment_name:
            self.config["gpt5"]["deployment_name"] = deployment_name
        self._save_config(self.config)
    
    def set_ollama_config(self, model: str, base_url: Optional[str] = None) -> None:
        """Set Ollama configuration."""
        self.config.setdefault("ollama", {})
        self.config["ollama"]["model"] = model
        if base_url:
            self.config["ollama"]["base_url"] = base_url
        self._save_config(self.config)
    
    def is_provider_enabled(self, provider: str) -> bool:
        """Check if a provider is enabled."""
        return self.config.get(provider, {}).get("enabled", True)
    
    def get_default_provider(self) -> str:
        """Get the default provider name."""
        return self.config.get("default_provider", "ollama")
    
    def is_fallback_enabled(self) -> bool:
        """Check if fallback between providers is enabled."""
        return self.config.get("fallback_enabled", True)