"""
GPT-5 AI Provider using Azure OpenAI
This provider interfaces with GPT-5 through Azure OpenAI API.
"""

import requests
import json
from typing import Optional
from .base_provider import BaseAIProvider


class GPT5Provider(BaseAIProvider):
    """GPT-5 provider using Azure OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None, **kwargs):
        """
        Initialize GPT-5 provider.
        
        Args:
            api_key: Azure OpenAI API key
            endpoint: Azure OpenAI endpoint URL
        """
        # Default configuration - users should replace with their own
        self.api_key = api_key or "your-azure-openai-api-key-here"
        self.endpoint = endpoint or "https://your-azure-openai-resource.openai.azure.com/"
        self.deployment_name = kwargs.get("deployment_name", "gpt-5")
        self.api_version = kwargs.get("api_version", "2024-02-15-preview")
        
        super().__init__("GPT-5", **kwargs)
    
    def _test_connection(self) -> bool:
        """Test connection to Azure OpenAI API."""
        if self.api_key == "your-azure-openai-api-key-here":
            print(f"⚠️  {self.name}: Please configure your Azure OpenAI API key")
            self.is_available = False
            return False
            
        try:
            # Test with a simple prompt
            test_response = self._make_api_call("Hello", max_tokens=5, temperature=0.1)
            if test_response and not test_response.startswith("Error"):
                self.is_available = True
                return True
        except Exception as e:
            print(f"⚠️  {self.name} connection test failed: {e}")
        
        self.is_available = False
        return False
    
    def _make_api_call(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> str:
        """Make API call to Azure OpenAI."""
        url = f"{self.endpoint}openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        data = {
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful voice assistant. Provide clear, concise answers."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            else:
                return "No response generated"
                
        except requests.RequestException as e:
            return f"Error: Network request failed - {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid response format"
        except KeyError as e:
            return f"Error: Unexpected response structure - {str(e)}"
    
    def generate_response(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> str:
        """Generate response using GPT-5."""
        if not self.is_available:
            return f"Error: {self.name} is not available. Please check your configuration."
        
        return self._make_api_call(prompt, max_tokens, temperature)
    
    def get_provider_info(self) -> dict:
        """Return information about the GPT-5 provider."""
        return {
            "name": self.name,
            "type": "cloud",
            "model": "GPT-5",
            "provider": "Azure OpenAI",
            "endpoint": self.endpoint,
            "deployment": self.deployment_name,
            "api_version": self.api_version,
            "available": self.is_available,
            "description": "GPT-5 model via Azure OpenAI API"
        }