#!/usr/bin/env python3
"""
Demo script for AI Providers
This script demonstrates the AI providers structure without requiring external services.
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from assistant.ai_providers import BaseAIProvider, GPT5Provider, OllamaProvider
    from assistant.ai_providers.manager import AIProviderManager
    from assistant.ai_providers.config import AIProvidersConfig
except ImportError as e:
    print(f"❌ Failed to import AI providers: {e}")
    sys.exit(1)


def demo_provider_structure():
    """Demonstrate the AI provider structure."""
    print("🚀 AI Voice Assistant - AI Providers Demo")
    print("=" * 60)
    
    print("\n📁 AI Providers Structure:")
    print("src/assistant/ai_providers/")
    print("├── __init__.py           # Module initialization")
    print("├── base_provider.py      # Abstract base class")
    print("├── gpt5_provider.py      # GPT-5 Azure OpenAI provider")
    print("├── ollama_provider.py    # Ollama local provider")
    print("├── config.py             # Configuration management")
    print("└── manager.py            # Provider management")
    
    print("\n🔧 Initializing Providers...")
    
    # Initialize individual providers
    gpt5 = GPT5Provider()
    ollama = OllamaProvider()
    
    # Show provider info
    providers = [gpt5, ollama]
    
    for provider in providers:
        info = provider.get_provider_info()
        print(f"\n📋 {provider.name} Provider:")
        print(f"   Type: {info['type']}")
        print(f"   Model: {info['model']}")
        print(f"   Available: {'✅' if provider.is_online() else '❌'}")
        print(f"   Description: {info['description']}")
    
    # Demonstrate manager
    print(f"\n🎛️  AI Provider Manager:")
    manager = AIProviderManager()
    status = manager.get_providers_status()
    
    print(f"   Registered providers: {list(status.keys())}")
    print(f"   Available providers: {manager.get_available_providers()}")
    primary = manager.get_primary_provider()
    if primary:
        print(f"   Primary provider: {primary.name}")
    else:
        print("   Primary provider: None (configure providers to enable)")
    
    # Demonstrate configuration
    print(f"\n⚙️  Configuration:")
    config = AIProvidersConfig()
    print(f"   Default provider: {config.get_default_provider()}")
    print(f"   Fallback enabled: {config.is_fallback_enabled()}")
    print(f"   GPT-5 enabled: {config.is_provider_enabled('gpt5')}")
    print(f"   Ollama enabled: {config.is_provider_enabled('ollama')}")
    
    print(f"\n📝 Sample Usage:")
    print("```python")
    print("# Initialize manager")
    print("manager = AIProviderManager()")
    print("")
    print("# Generate response with fallback")
    print("response, provider = manager.generate_response('Hello, how are you?')")
    print("print(f'Response from {provider}: {response}')")
    print("")
    print("# Use specific provider")
    print("gpt5_response = manager.generate_response('What is AI?', preferred_provider='gpt5')")
    print("```")
    
    print(f"\n✅ AI Providers structure is working correctly!")
    print("📖 Run 'python test_ai_providers.py' to test with actual providers")


if __name__ == "__main__":
    demo_provider_structure()