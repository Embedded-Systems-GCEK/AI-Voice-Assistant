"""
Integration Example: Using the new AI Providers system with the existing assistant
This example shows how to integrate the modular AI providers with the current assistant.
"""

import sys
import os
import datetime
import re
import threading

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from assistant.ai_providers import AIProviderManager
    from files import Files
    from status import Status
    # Try to import TTS, but handle platform-specific issues
    try:
        from tts import TTS
        TTS_AVAILABLE = True
    except ImportError:
        print("⚠️  TTS not available on this platform (missing winsound). Using text-only output.")
        TTS_AVAILABLE = False
        class TTS:
            def speak(self, text):
                print(f"🔊 TTS: {text}")
except ImportError as e:
    print(f"❌ Failed to import required modules: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


class ModernAssistant:
    """Updated Assistant class using the new AI Providers system."""
    
    def __init__(self, name: str = "Cyrus"):
        self.name = name
        self.status = Status()
        self.files = Files()
        self.tts = TTS()
        
        # Initialize the new AI providers system
        self.ai_manager = AIProviderManager()
        
        self.question = ""
        self.response = ""
        
        print(f"🤖 {self.name} initialized with AI Providers:")
        providers_status = self.ai_manager.get_providers_status()
        for provider_name, status in providers_status.items():
            availability = "✅ Available" if status["available"] else "❌ Not Available"
            print(f"   {provider_name}: {availability}")
    
    def process_command(self, query: str) -> None:
        """Process user command with the new AI providers system."""
        self.question = query
        if query == "":
            return
        
        # Check built-in dictionary responses first
        if query in self.files.qa_dictionary:
            self.speak(self.files.qa_dictionary[query])
            return
        
        # Handle time/date queries
        if "time" in query and "date" in query:
            self.tell_datetime()
            return
        elif "time" in query:
            self.tell_time()
            return
        elif "date" in query:
            self.tell_date()
            return
        elif "day" in query:
            self.tell_day()
            return
        
        # Use the new AI providers system for other queries
        self.get_ai_response(query)
    
    def get_ai_response(self, query: str) -> None:
        """Get AI response using the new providers system."""
        # Check if we're connected to prioritize cloud providers
        if self.status.is_connected:
            self.speak("Thinking...")
            # Try cloud providers first when online
            response, provider_used = self.ai_manager.generate_response(
                query, 
                max_tokens=50, 
                temperature=0.3, 
                preferred_provider="gpt5"
            )
        else:
            self.speak("I'm offline. Using local AI...")
            # Use local providers when offline
            response, provider_used = self.ai_manager.generate_response(
                query, 
                max_tokens=50, 
                temperature=0.3, 
                preferred_provider="ollama"
            )
        
        # Add provider info for transparency
        if provider_used != "none":
            print(f"💡 Response from {provider_used}")
        
        self.response = response
        self.speak(response)
    
    def speak(self, text):
        """Speak response using TTS."""
        self.response = text
        threading.Thread(target=self.print_history, daemon=True).start()
        
        # Clean unwanted characters for TTS
        clean_text = re.sub(r'[*_`~#>\\-]', '', text)
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', clean_text)
        self.tts.speak(clean_text)
    
    def tell_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {now}")

    def tell_date(self):
        today = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today's date is {today}")
    
    def tell_day(self):
        day = datetime.datetime.now().strftime("%A")
        self.speak(f"Today is {day}")
    
    def tell_datetime(self):
        dt = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        self.speak(f"The current date and time is {dt}")
    
    def print_history(self):
        print(f"Q: {self.question}")
        print(f"A: {self.response}")
        print("-" * 50)
    
    def get_ai_status(self) -> dict:
        """Get detailed status of AI providers."""
        return {
            "internet_connected": self.status.is_connected,
            "providers": self.ai_manager.get_providers_status(),
            "available_providers": self.ai_manager.get_available_providers(),
            "primary_provider": self.ai_manager.get_primary_provider().name if self.ai_manager.get_primary_provider() else None
        }


def demo_integration():
    """Demonstrate the integration with the new AI providers system."""
    print("🚀 AI Voice Assistant - Modern Integration Demo")
    print("=" * 60)
    
    # Initialize the modern assistant
    assistant = ModernAssistant()
    
    print(f"\n📊 AI Status:")
    status = assistant.get_ai_status()
    print(f"   Internet: {'Connected' if status['internet_connected'] else 'Offline'}")
    print(f"   Available Providers: {status['available_providers']}")
    print(f"   Primary Provider: {status['primary_provider']}")
    
    # Test queries
    test_queries = [
        "hello",
        "what time is it",
        "what is artificial intelligence",
        "tell me about machine learning",
        "what can you do"
    ]
    
    print(f"\n🧪 Testing Integration with Sample Queries:")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n👤 User: {query}")
        assistant.process_command(query.lower())
    
    print(f"\n✅ Integration demo completed!")
    print(f"📖 The assistant now uses the modular AI providers system")


def show_migration_guide():
    """Show how to migrate from the old system to the new one."""
    print(f"\n🔄 Migration Guide: Old vs New System")
    print("=" * 60)
    
    print(f"\n📜 OLD SYSTEM (assistant.py):")
    print("```python")
    print("# Old way - hardcoded providers")
    print("from cohere_api import ask_cohere")
    print("from ollama import Ollama")
    print("")
    print("if self.status.is_connected:")
    print("    response = ask_cohere(query)")
    print("else:")
    print("    response = self.ollama.ask_ollama(query)")
    print("```")
    
    print(f"\n🆕 NEW SYSTEM (with AI Providers):")
    print("```python")
    print("# New way - modular providers with fallback")
    print("from assistant.ai_providers import AIProviderManager")
    print("")
    print("ai_manager = AIProviderManager()")
    print("response, provider = ai_manager.generate_response(")
    print("    query,")
    print("    preferred_provider='gpt5' if online else 'ollama'")
    print(")")
    print("```")
    
    print(f"\n✨ Benefits of New System:")
    print("• ✅ Modular and extensible")
    print("• ✅ Automatic fallback between providers") 
    print("• ✅ Configuration management")
    print("• ✅ Health monitoring")
    print("• ✅ Easy to add new providers")
    print("• ✅ Better error handling")
    print("• ✅ Comprehensive testing")


if __name__ == "__main__":
    demo_integration()
    show_migration_guide()