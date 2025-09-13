# AI Providers Module

This module provides a modular AI provider system for the AI Voice Assistant, supporting multiple AI models with automatic fallback capabilities.

## Supported Providers

### GPT-5 (Azure OpenAI)
- **Type**: Cloud-based
- **Model**: GPT-5
- **Provider**: Azure OpenAI API
- **Requirements**: Azure OpenAI API key and endpoint

### Ollama (Local Inference)
- **Type**: Local
- **Model**: Configurable (default: mistral:7b)  
- **Provider**: Ollama local server
- **Requirements**: Ollama installation and downloaded models

## Quick Start

### 1. Basic Usage

```python
from assistant.ai_providers import AIProviderManager

# Initialize the manager
manager = AIProviderManager()

# Generate response with automatic provider selection
response, provider_used = manager.generate_response("Hello, how are you?")
print(f"Response from {provider_used}: {response}")
```

### 2. Provider-Specific Usage

```python
from assistant.ai_providers import GPT5Provider, OllamaProvider

# Use GPT-5 specifically
gpt5 = GPT5Provider(
    api_key="your-api-key",
    endpoint="https://your-resource.openai.azure.com/"
)

if gpt5.is_online():
    response = gpt5.generate_response("What is AI?")
    print(response)

# Use Ollama specifically  
ollama = OllamaProvider(model="mistral:7b")
if ollama.is_online():
    response = ollama.generate_response("Explain machine learning")
    print(response)
```

## Configuration

### Environment Variables

Set these environment variables for automatic configuration:

```bash
# GPT-5 / Azure OpenAI
export AZURE_OPENAI_API_KEY="your-api-key-here"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="gpt-5"

# Ollama
export OLLAMA_MODEL="mistral:7b"
export OLLAMA_BASE_URL="http://localhost:11434"
```

### Configuration File

The system creates and uses `ai_providers_config.json` for persistent configuration:

```json
{
  "gpt5": {
    "api_key": "your-azure-openai-api-key-here",
    "endpoint": "https://your-azure-openai-resource.openai.azure.com/",
    "deployment_name": "gpt-5",
    "api_version": "2024-02-15-preview",
    "enabled": true
  },
  "ollama": {
    "model": "mistral:7b",
    "base_url": "http://localhost:11434",
    "use_api": true,
    "enabled": true
  },
  "default_provider": "ollama",
  "fallback_enabled": true
}
```

## Setup Instructions

### GPT-5 Setup

1. Get Azure OpenAI access and API key from [GitHub Marketplace](https://github.com/marketplace/models/azure-openai/gpt-5)
2. Create an Azure OpenAI resource
3. Deploy the GPT-5 model
4. Configure your credentials:

```python
from assistant.ai_providers import AIProvidersConfig

config = AIProvidersConfig()
config.set_gpt5_credentials(
    api_key="your-api-key",
    endpoint="https://your-resource.openai.azure.com/",
    deployment_name="gpt-5"
)
```

### Ollama Setup

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Download and run a model:
   ```bash
   ollama run mistral:7b
   ```
3. Verify it's running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

## Testing

Run the test scripts to verify your setup:

```bash
# Test all providers
python test_ai_providers.py

# Demo the structure (no external dependencies required)
python demo_ai_providers.py
```

## Provider Manager Features

- **Automatic Fallback**: If primary provider fails, automatically tries backup providers
- **Health Monitoring**: Continuously monitors provider availability
- **Load Balancing**: Can distribute requests across multiple providers  
- **Configuration Management**: Centralized configuration for all providers
- **Extensible**: Easy to add new AI providers

## Adding Custom Providers

1. Inherit from `BaseAIProvider`:

```python
from assistant.ai_providers.base_provider import BaseAIProvider

class MyCustomProvider(BaseAIProvider):
    def __init__(self, **kwargs):
        super().__init__("MyProvider", **kwargs)
    
    def _test_connection(self) -> bool:
        # Test your provider connection
        return True
    
    def generate_response(self, prompt: str, max_tokens: int = 50, temperature: float = 0.3) -> str:
        # Generate response using your provider
        return "Custom response"
    
    def get_provider_info(self) -> dict:
        return {
            "name": self.name,
            "type": "custom",
            "model": "custom-model",
            "available": self.is_available
        }
```

2. Add to the manager:

```python
manager = AIProviderManager()
manager.add_provider("custom", MyCustomProvider())
```

## File Structure

```
src/assistant/ai_providers/
├── __init__.py           # Module exports
├── base_provider.py      # Abstract base class
├── gpt5_provider.py      # GPT-5 Azure OpenAI provider
├── ollama_provider.py    # Ollama local provider
├── config.py             # Configuration management
├── manager.py            # Provider management and fallback
└── README.md             # This file
```

## Error Handling

The system provides comprehensive error handling:

- **Connection Errors**: Automatic fallback to available providers
- **API Errors**: Graceful error messages and provider switching
- **Configuration Errors**: Clear setup guidance and validation
- **Timeout Handling**: Configurable timeouts for all providers

## Best Practices

1. **Always use the AIProviderManager** for automatic fallback support
2. **Set up both local and cloud providers** for maximum reliability
3. **Use environment variables** for sensitive configuration
4. **Test your setup** regularly with the provided test scripts
5. **Monitor provider availability** in production environments