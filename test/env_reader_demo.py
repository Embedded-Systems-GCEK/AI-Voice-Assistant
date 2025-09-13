#!/usr/bin/env python3
"""
Environment Variables Reader for AI Voice Assistant
Demonstrates how to read .env files and environment variables in Python
"""

import os
from dotenv import load_dotenv
from pathlib import Path

def load_environment_variables():
    """Load environment variables from .env file"""
    # Get the project root directory (current directory, not parent)
    project_root = Path(__file__).parent
    print(f"🏠 Project Root: {project_root}")
    # Load .env file from project root
    env_path = project_root / '.env'
    load_dotenv(env_path)

    print("🔧 Loading environment variables...")
    print(f"📁 .env file path: {env_path}")
    print(f"📁 .env file exists: {env_path.exists()}")
    print()

def get_github_token():
    """Get GitHub token from environment"""
    token = os.getenv('GITHUB_GPT_5_TOKEN')

    if token:
        print("✅ GitHub Token Found!")
        print(f"🔑 Token: {token[:20]}...{token[-4:] if len(token) > 24 else token}")
        return token
    else:
        print("❌ GitHub Token Not Found!")
        return None

def get_cohere_key():
    """Get Cohere API key from environment"""
    key = os.getenv('COHERE_API_KEY')

    if key:
        print("✅ Cohere API Key Found!")
        print(f"🔑 Key: {key[:10]}...{key[-4:] if len(key) > 14 else key}")
        return key
    else:
        print("❌ Cohere API Key Not Found!")
        return None

def get_ollama_config():
    """Get Ollama configuration from environment"""
    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'tinyllama')

    print("🤖 Ollama Configuration:")
    print(f"   URL: {base_url}")
    print(f"   Model: {model}")

    return base_url, model

def demonstrate_env_reading():
    """Demonstrate different ways to read environment variables"""

    print("=" * 60)
    print("🌟 ENVIRONMENT VARIABLES READER DEMO")
    print("=" * 60)
    print()

    # Load environment variables
    load_environment_variables()

    # Demonstrate reading specific variables
    print("🔍 Reading Specific Variables:")
    print("-" * 30)

    github_token = get_github_token()
    print()

    cohere_key = get_cohere_key()
    print()

    ollama_url, ollama_model = get_ollama_config()
    print()

    # Show all environment variables (be careful with sensitive data!)
    print("📋 All Environment Variables (non-sensitive):")
    print("-" * 50)

    safe_vars = ['OLLAMA_BASE_URL', 'OLLAMA_MODEL', 'PATH', 'PYTHONPATH']
    for var in safe_vars:
        value = os.getenv(var)
        if value:
            print(f"   {var}: {value}")

    print()
    print("✅ Environment variables loaded successfully!")

    return {
        'github_token': github_token,
        'cohere_key': cohere_key,
        'ollama_url': ollama_url,
        'ollama_model': ollama_model
    }

if __name__ == "__main__":
    try:
        config = demonstrate_env_reading()

        print("\n🎯 Usage Examples:")
        print("-" * 20)
        print("# In your code:")
        print("from dotenv import load_dotenv")
        print("import os")
        print()
        print("load_dotenv()  # Load .env file")
        print("token = os.getenv('GITHUB_GPT_5_TOKEN')")
        print("key = os.getenv('COHERE_API_KEY')")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure you have python-dotenv installed:")
        print("   pip install python-dotenv")
