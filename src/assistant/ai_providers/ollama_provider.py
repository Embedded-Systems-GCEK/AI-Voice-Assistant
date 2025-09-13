"""
Ollama AI Provider for Local Inference
This provider interfaces with locally running Ollama models.
"""

import subprocess
import requests
import json
from typing import Optional
from .base_provider import BaseAIProvider


class OllamaProvider(BaseAIProvider):
    """Ollama provider for local AI inference."""
    
    def __init__(self, model: str = "mistral:7b", base_url: str = "http://localhost:11434", **kwargs):
        """
        Initialize Ollama provider.
        
        Args:
            model: Ollama model name (e.g., 'mistral:7b', 'llama2', 'codellama')
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        self.use_api = kwargs.get("use_api", True)  # Use API by default, fallback to CLI
        
        super().__init__("Ollama", **kwargs)
    
    def _test_connection(self) -> bool:
        """Test connection to Ollama."""
        # First try API method
        if self._test_api_connection():
            self.use_api = True
            self.is_available = True
            return True
        
        # Fallback to CLI method
        if self._test_cli_connection():
            self.use_api = False
            self.is_available = True
            return True
        
        self.is_available = False
        return False
    
    def _test_api_connection(self) -> bool:
        """Test connection using Ollama REST API."""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                # Check if our model is available
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                if self.model in model_names:
                    return True
                else:
                    print(f"⚠️  Ollama: Model '{self.model}' not found. Available models: {model_names}")
                    return False
        except Exception as e:
            print(f"⚠️  Ollama API test failed: {e}")
        return False
    
    def _test_cli_connection(self) -> bool:
        """Test connection using Ollama CLI."""
        try:
            result = subprocess.run(
                ["ollama", "list"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0 and self.model.split(':')[0] in result.stdout:
                return True
        except Exception as e:
            print(f"⚠️  Ollama CLI test failed: {e}")
        return False
    
    def _generate_via_api(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> str:
        """Generate response using Ollama REST API."""
        try:
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model,
                "prompt": f"Answer clearly and briefly: {prompt}",
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "response" in result:
                return result["response"].strip()
            else:
                return "No response generated"
                
        except Exception as e:
            return f"Error: Ollama API request failed - {str(e)}"
    
    def _generate_via_cli(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> str:
        """Generate response using Ollama CLI (fallback method)."""
        try:
            formatted_prompt = f"Answer clearly and briefly: {prompt}"
            result = subprocess.run(
                f"echo {formatted_prompt!r} | ollama run {self.model}",
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"Ollama CLI error: {result.stderr}")
                return "Sorry, I couldn't get a response."
            
            # Clean and format the response
            lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            # Take first few lines to respect max_tokens roughly
            response_lines = lines[:3] if max_tokens <= 50 else lines[:5]
            return ' '.join(response_lines)
            
        except subprocess.TimeoutExpired:
            return "Error: Response timeout"
        except Exception as e:
            return f"Error communicating with Ollama: {e}"
    
    def generate_response(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> str:
        """Generate response using Ollama."""
        if not self.is_available:
            return f"Error: {self.name} is not available. Please ensure Ollama is running and '{self.model}' is installed."
        
        if self.use_api:
            return self._generate_via_api(prompt, max_tokens, temperature)
        else:
            return self._generate_via_cli(prompt, max_tokens, temperature)
    
    def get_provider_info(self) -> dict:
        """Return information about the Ollama provider."""
        return {
            "name": self.name,
            "type": "local",
            "model": self.model,
            "provider": "Ollama",
            "base_url": self.base_url,
            "method": "API" if self.use_api else "CLI",
            "available": self.is_available,
            "description": f"Local {self.model} model via Ollama"
        }