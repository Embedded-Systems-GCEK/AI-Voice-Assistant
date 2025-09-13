#!/usr/bin/env python3
"""
Test script for AI Providers
This script tests the GPT-5 and Ollama providers to ensure they work correctly.
"""

import os
import sys
import json
from typing import List, Dict

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from assistant.ai_providers import BaseAIProvider, GPT5Provider, OllamaProvider
except ImportError as e:
    print(f"❌ Failed to import AI providers: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


def test_provider(provider: BaseAIProvider, test_questions: List[str]) -> Dict:
    """Test a single AI provider with a set of questions."""
    print(f"\n🧪 Testing {provider.name} Provider")
    print("=" * 50)
    
    # Get provider info
    info = provider.get_provider_info()
    print(f"Provider Type: {info.get('type', 'unknown')}")
    print(f"Model: {info.get('model', 'unknown')}")
    print(f"Available: {'✅ Yes' if provider.is_online() else '❌ No'}")
    
    results = {
        "provider": provider.name,
        "available": provider.is_online(),
        "info": info,
        "tests": []
    }
    
    if not provider.is_online():
        print(f"⚠️  Skipping tests - {provider.name} is not available")
        return results
    
    # Test each question
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {question}")
        try:
            response = provider.generate_response(question, max_tokens=50, temperature=0.3)
            print(f"💬 Response: {response}")
            
            test_result = {
                "question": question,
                "response": response,
                "success": not response.startswith("Error")
            }
            results["tests"].append(test_result)
            
            if test_result["success"]:
                print("✅ Test passed")
            else:
                print("❌ Test failed")
                
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results["tests"].append({
                "question": question,
                "response": f"Exception: {e}",
                "success": False
            })
    
    return results


def main():
    """Main test function."""
    print("🚀 AI Voice Assistant - AI Providers Test")
    print("=" * 60)
    
    # Test questions
    test_questions = [
        "Hello, how are you?",
        "What is Python?",
        "Tell me a fun fact",
        "What's 2+2?",
        "What is AI?"
    ]
    
    # Initialize providers
    print("\n🔧 Initializing AI Providers...")
    
    # GPT-5 Provider
    gpt5_provider = GPT5Provider()
    
    # Ollama Provider  
    ollama_provider = OllamaProvider(model="mistral:7b")
    
    # Test providers
    all_results = []
    
    # Test GPT-5
    gpt5_results = test_provider(gpt5_provider, test_questions)
    all_results.append(gpt5_results)
    
    # Test Ollama
    ollama_results = test_provider(ollama_provider, test_questions)
    all_results.append(ollama_results)
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    for result in all_results:
        provider_name = result["provider"]
        available = result["available"]
        successful_tests = sum(1 for test in result["tests"] if test["success"])
        total_tests = len(result["tests"])
        
        print(f"\n{provider_name}:")
        print(f"  Available: {'✅ Yes' if available else '❌ No'}")
        if available:
            print(f"  Tests Passed: {successful_tests}/{total_tests}")
            if successful_tests == total_tests:
                print(f"  Status: ✅ All tests passed!")
            else:
                print(f"  Status: ⚠️  Some tests failed")
        else:
            print(f"  Status: ⚠️  Provider not available for testing")
    
    # Save detailed results
    results_file = "test_results.json"
    try:
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        print(f"\n💾 Detailed results saved to {results_file}")
    except Exception as e:
        print(f"⚠️  Could not save results: {e}")
    
    # Configuration guidance
    print("\n⚙️  Configuration Guidance")
    print("=" * 50)
    
    if not gpt5_results["available"]:
        print("\n🔑 GPT-5 Setup:")
        print("1. Get your Azure OpenAI API key from:")
        print("   https://github.com/marketplace/models/azure-openai/gpt-5")
        print("2. Update the GPT5Provider initialization with your credentials:")
        print("   gpt5_provider = GPT5Provider(")
        print("       api_key='your-api-key-here',")
        print("       endpoint='https://your-resource.openai.azure.com/'")
        print("   )")
    
    if not ollama_results["available"]:
        print("\n🦙 Ollama Setup:")
        print("1. Install Ollama from: https://ollama.ai/")
        print("2. Download the Mistral model:")
        print("   ollama run mistral:7b")
        print("3. Ensure Ollama is running in the background")


if __name__ == "__main__":
    main()