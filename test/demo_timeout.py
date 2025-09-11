"""
Simple demonstration of the timeout functionality.
Run this to see how the 10-second timeout and prompting works.
"""

# Mock classes for demonstration purposes (replace with actual imports)
class MockTTS:
    def speak(self, text):
        print(f"🔊 Assistant says: {text}")

class MockStatus:
    def __init__(self):
        self.connected = True
    
    @property
    def is_connected(self):
        return self.connected

class MockOllama:
    def ask_ollama(self, query):
        return f"Local response to: {query}"

class MockFiles:
    def __init__(self):
        self.qa_dictionary = {
            "hello": "Hello there!",
            "how are you": "I'm doing great, thank you for asking!"
        }

def mock_ask_cohere(query):
    return f"Cohere response to: {query}"

# Demonstration
def demonstrate_timeout():
    print("=== AI Voice Assistant Timeout Demo ===")
    print("This shows how the assistant behaves with timeout functionality.")
    print("-" * 60)
    
    # Mock the assistant components
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Replace the ask_cohere function temporarily
    import builtins
    builtins.ask_cohere = mock_ask_cohere
    
    from src.assistant.assistant import ConversationalAssistant
    
    # Initialize with mock objects
    status = MockStatus()
    tts = MockTTS()
    ollama = MockOllama()
    files = MockFiles()
    
    assistant = ConversationalAssistant(
        name="DEMO_ASSISTANT",
        voice_config=None,
        status=status,
        tts=tts,
        ollama=ollama,
        files=files
    )
    assistant.set_timeout(3)  # Short timeout for demo
    
    print("1. Initial greeting:")
    assistant.greet()
    print()
    
    print("2. Demonstrating name extraction:")
    assistant.process_command("my name is Alice")
    print()
    
    print("3. Demonstrating personalized response:")
    assistant.process_command("what time is it")
    print()
    
    print("4. Demonstrating prompting when no name is known:")
    assistant.reset_conversation()
    assistant.ask_next_prompt()
    print()
    
    print("5. Conversation info:")
    info = assistant.get_conversation_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    print()
    
    print("6. Demonstrating different prompt questions:")
    assistant.user_name = "Bob"
    for i in range(3):
        assistant.ask_next_prompt()
    
    print("\n" + "=" * 60)
    print("Demo complete! This shows how the timeout and prompting system works.")
    print("In real usage, the assistant would listen for 10 seconds before prompting.")

if __name__ == "__main__":
    demonstrate_timeout()
