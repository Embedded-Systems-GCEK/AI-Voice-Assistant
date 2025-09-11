import speech_recognition as sr
from assistant.cohere_api import ask_cohere
import datetime
import re
from assistant.status import Status
from assistant.tts import TTS
from assistant.ollama import Ollama
from assistant.files import Files
import threading
import time
import signal
import sys
class Assistant:
    def __init__(self, status: Status, name: str, tts: TTS, ollama: Ollama, files: Files):
        self.status: Status = status
        self.name: str = name
        self.tts: TTS = tts
        self.ollama: Ollama = ollama
        self.files = files
        self.recognizer: sr.Recognizer = sr.Recognizer()
        self.question: str = ""
        self.response: str = ""
        self.user_name: str = ""
        self.conversation_state: str = "waiting"  # waiting, listening, processing
        self.timeout_seconds: int = 10
        self.prompts = [
            "What's your name?",
            "How are you feeling today?",
            "What would you like to know?",
            "Is there anything I can help you with?",
            "Tell me about your day.",
            "What are your hobbies?"
        ]
        self.current_prompt_index: int = 0
    def run(self):
        self.conversation_state = "waiting"
        while True:
            try:
                query: str = self.listen_with_timeout()
                if query:
                    self.process_command(query)
                else:
                    # No input received within timeout, ask a prompt
                    self.ask_next_prompt()
                time.sleep(1)  # Brief pause between cycles
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(2)

    def listen_with_timeout(self) -> str:
        """Listen for user input with a timeout mechanism"""
        self.conversation_state = "listening"
        print(f"Listening... (timeout in {self.timeout_seconds} seconds)")
        
        try:
            with sr.Microphone() as source:
                self.recognizer.pause_threshold = 0.5
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=self.timeout_seconds, phrase_time_limit=6)
            
            try:
                command = self.recognizer.recognize_google(audio, language='en-US')
                print(f"You said: {command}")
                self.conversation_state = "processing"
                return command.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return ""
            except sr.RequestError:
                self.speak("Speech service is unavailable.")
                return ""
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            self.conversation_state = "waiting"
            return ""
        except Exception as e:
            print(f"Error during listening: {e}")
            return ""

    def ask_next_prompt(self):
        """Ask the next prompt question when no input is received"""
        if not self.user_name:
            prompt = "Hi there! What's your name?"
        else:
            prompt = f"Hi {self.user_name}! " + self.prompts[self.current_prompt_index]
            self.current_prompt_index = (self.current_prompt_index + 1) % len(self.prompts)
        
        self.speak(prompt)
        print(f"Asked prompt: {prompt}")

    def set_timeout(self, seconds: int):
        """Set the timeout duration in seconds"""
        self.timeout_seconds = seconds
        print(f"Timeout set to {seconds} seconds")
    def is_connected(self) -> bool:
        return self.status.connected
    def greet(self):
        greeting: str = f"Hello, I am {self.name}. How can I assist you today?"
        self.tts.speak(greeting)
    def listen(self) -> str:
        """Legacy listen method for backward compatibility"""
        return self.listen_with_timeout()

    def extract_name_from_response(self, query: str) -> bool:
        """Extract name from user response and store it"""
        # Simple name extraction patterns
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)",
            r"(\w+) is my name"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                self.user_name = match.group(1).capitalize()
                self.speak(f"Nice to meet you, {self.user_name}!")
                return True
        
        # If no pattern matches but it seems like they're responding to name question
        if not self.user_name and any(word in query for word in ["name", "call", "i'm", "i am"]):
            # Try to extract the last word as potential name
            words = query.split()
            if len(words) > 0:
                potential_name = words[-1].strip('.,!?').capitalize()
                if len(potential_name) > 1 and potential_name.isalpha():
                    self.user_name = potential_name
                    self.speak(f"Nice to meet you, {self.user_name}!")
                    return True
        
        return False
    def speak(self, text):
        self.response = text
        threading.Thread(target=self.print_history, daemon=True).start()
        # Clean unwanted chars
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
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        user_prefix = f"{self.user_name}: " if self.user_name else "User: "
        print(f"[{timestamp}] {user_prefix}{self.question}")
        print(f"[{timestamp}] {self.name}: {self.response}\n")
    
    def get_conversation_info(self) -> dict:
        """Get current conversation state information"""
        return {
            "user_name": self.user_name,
            "conversation_state": self.conversation_state,
            "timeout_seconds": self.timeout_seconds,
            "current_prompt_index": self.current_prompt_index,
            "assistant_name": self.name,
            "is_connected": self.status.is_connected
        }
    
    def reset_conversation(self):
        """Reset conversation state (useful for testing)"""
        self.user_name = ""
        self.conversation_state = "waiting"
        self.current_prompt_index = 0
        self.speak("Conversation reset. Hello! What's your name?")
    
    def is_waiting_for_input(self) -> bool:
        """Check if assistant is currently waiting for user input"""
        return self.conversation_state == "waiting"
        
    def process_command(self, query: str) -> None:
        self.question = query
        if query == "":
            return

        # Try to extract name if we don't have one yet
        if not self.user_name:
            if self.extract_name_from_response(query):
                return

        # Check for predefined Q&A
        if query in self.files.qa_dictionary:
            response = self.files.qa_dictionary[query]
            if self.user_name:
                response = f"{self.user_name}, {response}"
            self.speak(response)
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

        # Handle goodbye/exit commands
        if any(word in query for word in ["goodbye", "bye", "exit", "quit", "stop"]):
            farewell = f"Goodbye, {self.user_name}!" if self.user_name else "Goodbye!"
            self.speak(farewell)
            return

        # Handle name-related queries
        if "what" in query and "name" in query:
            if self.user_name:
                self.speak(f"Your name is {self.user_name}.")
            else:
                self.speak("I don't know your name yet. What should I call you?")
            return

        # Use AI to respond
        if self.status.is_connected:
            self.speak("Let me think about that...")
            response = ask_cohere(query)
            # Personalize response if we have user's name
            if self.user_name and not response.startswith(self.user_name):
                response = f"{self.user_name}, {response}"
        else:
            self.speak("I'm offline. Thinking locally...")
            response = self.ollama.ask_ollama(query)
            if self.user_name and not response.startswith(self.user_name):
                response = f"{self.user_name}, {response}"
        
        self.response = response
        self.speak(self.response)
