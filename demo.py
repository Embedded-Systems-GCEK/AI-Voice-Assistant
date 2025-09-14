#!/usr/bin/env python3
"""
AI Voice Assistant Demo Mode
This version works without speech recognition or TTS for testing core functionality
"""

import sys
import os
import json
import datetime
import re
import subprocess
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class MockTTS:
    """Mock TTS class that just prints text instead of speaking"""
    def speak(self, text):
        print(f"🗣️  Assistant says: {text}")

class MockSpeechRecognition:
    """Mock speech recognition that uses text input"""
    def listen(self):
        try:
            user_input = input("🎤 You say: ").strip()
            return user_input.lower() if user_input else ""
        except KeyboardInterrupt:
            return "exit"
        except EOFError:
            return "exit"

class DemoAssistant:
    """Simplified assistant for demo purposes"""
    
    def __init__(self):
        self.name = "Cyrus"
        self.tts = MockTTS()
        self.speech = MockSpeechRecognition()
        self.dictionaries = self.load_dictionaries()
        self.running = True
        
    def load_dictionaries(self):
        """Load Q&A dictionaries"""
        try:
            with open('dictionaries.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading dictionaries: {e}")
            return {}
    
    def check_internet(self):
        """Check if internet is available"""
        try:
            import urllib.request
            urllib.request.urlopen("https://www.google.com", timeout=3)
            return True
        except:
            return False
    
    def tell_time(self):
        """Tell the current time"""
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}"
    
    def tell_date(self):
        """Tell the current date"""
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {today}"
    
    def tell_day(self):
        """Tell the current day"""
        day = datetime.datetime.now().strftime("%A")
        return f"Today is {day}"
    
    def tell_datetime(self):
        """Tell the current date and time"""
        dt = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        return f"The current date and time is {dt}"
    
    def ask_cohere(self, query):
        """Try to ask Cohere AI"""
        try:
            # Import cohere if available
            import cohere
            from src.cohere_api import ask_cohere
            return ask_cohere(query)
        except ImportError:
            return "Cohere AI is not available. Please install the 'cohere' package."
        except Exception as e:
            return f"Error with Cohere AI: {e}"
    
    def ask_ollama(self, query):
        """Try to ask Ollama"""
        try:
            formatted_prompt = f"Answer clearly and briefly: {query}"
            result = subprocess.run(
                f"echo {formatted_prompt!r} | ollama run mistral:7b",
                shell=True, capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                return ' '.join(lines[:3])
            else:
                return "Ollama is not available or not responding."
        except subprocess.TimeoutExpired:
            return "Ollama response timed out."
        except Exception as e:
            return f"Error with Ollama: {e}"
    
    def process_query(self, query):
        """Process a user query and return response"""
        if not query:
            return ""
        
        # Check exit conditions
        if query in ["exit", "quit", "goodbye", "bye"]:
            self.running = False
            return "Goodbye! Thank you for trying the AI Voice Assistant."
        
        # Check dictionaries first
        if query in self.dictionaries:
            return self.dictionaries[query]
        
        # Handle time/date queries
        if "time" in query and "date" in query:
            return self.tell_datetime()
        elif "time" in query:
            return self.tell_time()
        elif "date" in query:
            return self.tell_date()
        elif "day" in query:
            return self.tell_day()
        
        # Try AI responses
        if self.check_internet():
            print("🌐 Checking online AI...")
            response = self.ask_cohere(query)
            if "error" not in response.lower():
                return response
            print("🤖 Falling back to offline AI...")
            return self.ask_ollama(query)
        else:
            print("📱 No internet, using offline AI...")
            return self.ask_ollama(query)
    
    def greet(self):
        """Greet the user"""
        greeting = f"Hello! I am {self.name}, your AI voice assistant."
        self.tts.speak(greeting)
        self.tts.speak("Since this is demo mode, I'll print my responses instead of speaking.")
        self.tts.speak("Type your questions and I'll do my best to answer them!")
        self.tts.speak("Type 'exit' to quit.")
    
    def run(self):
        """Run the demo assistant"""
        self.greet()
        
        while self.running:
            try:
                # Get user input (mock "listening")
                query = self.speech.listen()
                
                if not query:
                    continue
                
                print(f"Processing: '{query}'")
                
                # Process the query
                response = self.process_query(query)
                
                if response:
                    # Clean the response
                    clean_response = re.sub(r'[*_`~#>\\-]', '', response)
                    clean_response = re.sub(r'[\U00010000-\U0010ffff]', '', clean_response)
                    
                    # "Speak" the response (print it)
                    self.tts.speak(clean_response)
                
            except KeyboardInterrupt:
                break
        
        print("\nDemo session ended. Thank you for trying the AI Voice Assistant!")

def main():
    """Main demo function"""
    print("🎙️ AI Voice Assistant - Demo Mode")
    print("="*50)
    print("This demo runs without speech recognition or TTS")
    print("You can type your questions instead of speaking")
    print("Responses will be printed instead of spoken")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists('dictionaries.json'):
        print("❌ Error: dictionaries.json not found")
        print("Please run this script from the AI-Voice-Assistant directory")
        return 1
    
    if not os.path.exists('src'):
        print("❌ Error: src directory not found")
        print("Please run this script from the AI-Voice-Assistant directory")
        return 1
    
    # Start the demo
    assistant = DemoAssistant()
    assistant.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())