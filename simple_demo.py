#!/usr/bin/env python3
"""
Simple AI Providers Integration Demo
This demo focuses purely on the AI providers functionality without TTS or audio.
"""

import sys
import os
import datetime

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from assistant.ai_providers import AIProviderManager
    from files import Files
except ImportError as e:
    print(f"❌ Failed to import required modules: {e}")
    sys.exit(1)


class SimpleAssistantDemo:
    """Simple demo of AI providers integration."""
    
    def __init__(self):
        self.files = Files()
        self.ai_manager = AIProviderManager()
        
        print("🤖 Simple AI Assistant Demo")
        print("=" * 40)
        self._show_provider_status()
    
    def _show_provider_status(self):
        """Show status of all AI providers."""
        providers_status = self.ai_manager.get_providers_status()
        print(f"\n📊 AI Provider Status:")
        for provider_name, status in providers_status.items():
            availability = "✅ Available" if status["available"] else "❌ Not Available"
            model = status["info"].get("model", "Unknown")
            provider_type = status["info"].get("type", "unknown")
            print(f"   {provider_name}: {availability} ({provider_type}, {model})")
        
        available = self.ai_manager.get_available_providers()
        primary = self.ai_manager.get_primary_provider()
        print(f"\n   Available: {available}")
        print(f"   Primary: {primary.name if primary else 'None'}")
    
    def process_query(self, query: str) -> str:
        """Process a query using the AI providers system."""
        # Check built-in responses first
        if query in self.files.qa_dictionary:
            return f"📚 Built-in: {self.files.qa_dictionary[query]}"
        
        # Handle time/date queries
        if "time" in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"⏰ Time: {now}"
        elif "date" in query:
            today = datetime.datetime.now().strftime("%B %d, %Y")
            return f"📅 Date: {today}"
        
        # Use AI providers for other queries
        response, provider_used = self.ai_manager.generate_response(
            query, 
            max_tokens=100, 
            temperature=0.3
        )
        
        if provider_used != "none":
            return f"🤖 {provider_used}: {response}"
        else:
            return f"⚠️ No AI: {response}"
    
    def interactive_demo(self):
        """Run an interactive demo."""
        print(f"\n💬 Interactive Demo (type 'quit' to exit):")
        print("=" * 40)
        
        while True:
            try:
                query = input("\n👤 You: ").strip().lower()
                if query in ['quit', 'exit', '']:
                    break
                
                response = self.process_query(query)
                print(f"🎙️ Assistant: {response}")
                
            except KeyboardInterrupt:
                break
        
        print("\n👋 Demo ended!")
    
    def run_test_queries(self):
        """Run predefined test queries."""
        test_queries = [
            "hello",
            "what time is it",
            "what is python programming",
            "tell me about AI",
            "what can you do"
        ]
        
        print(f"\n🧪 Test Queries:")
        print("=" * 40)
        
        for query in test_queries:
            print(f"\n👤 Query: {query}")
            response = self.process_query(query)
            print(f"🎙️ Response: {response}")


def main():
    """Main demo function."""
    demo = SimpleAssistantDemo()
    
    # Run test queries
    demo.run_test_queries()
    
    # Show setup instructions if no providers are available
    if not demo.ai_manager.get_available_providers():
        print(f"\n⚠️ Setup Required:")
        print("=" * 40)
        print("No AI providers are currently available. To test:")
        print("")
        print("🔑 GPT-5 Setup:")
        print("1. Get Azure OpenAI API key from:")
        print("   https://github.com/marketplace/models/azure-openai/gpt-5")
        print("2. Set environment variables:")
        print("   export AZURE_OPENAI_API_KEY='your-key'")
        print("   export AZURE_OPENAI_ENDPOINT='your-endpoint'")
        print("")
        print("🦙 Ollama Setup:")
        print("1. Install Ollama from: https://ollama.ai/")
        print("2. Run: ollama run mistral:7b")
        print("")
        print("Then run this demo again to see AI responses!")
    else:
        # Run interactive demo if providers are available
        demo.interactive_demo()


if __name__ == "__main__":
    main()