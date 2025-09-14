"""
Assistant Module

This module contains the concrete implementation of the ConversationalAssistant class.
It provides a complete conversational AI assistant with speech recognition, 
response generation, and conversation management.
"""

import speech_recognition as sr
import datetime
import re
import threading
import time
from typing import Optional

# Import the abstract base class from robo_types
from robot.assistant_robo import ASSISTANT, VoiceConfig
from robot.answer_helper.answer_helper import AnswerHelper
from robot.question_helper.question_helper import QuestionHelper
from files.files import Files




class ConversationalAssistant(ASSISTANT):
    """
    Concrete implementation of an AI assistant with full conversation capabilities.
    This class implements all the abstract methods from ASSISTANT and provides
    a complete conversational AI assistant with speech recognition, response generation,
    and conversation management.
    """
    
    def __init__(
        self,
        files: Files,
        answer_helper: AnswerHelper,
        question_helper: QuestionHelper,
        name: str = "Conversational Assistant"
    ):
        super().__init__(
            name=name,
            answer_helper=answer_helper,
            question_helper=question_helper,
            )
        self.files = files
        """Only Conversational Assistant Returns Something"""
        self.response = ""
        self.current_prompt_index = 0

    def greet(self) -> None:
        """Perform a greeting sequence"""
        greeting = f"Hello, I am {self.name}. How can I assist you today?"
        self.speak(greeting)

    def answer(self, text: str) -> None:
        """
        Speak the given text and manage conversation history.
        
        Args:
            text: The text to speak
            
        Returns:
            bool: True if speech was successful, False otherwise
        """
        self.response = text
        # Clean unwanted characters
        clean_text = re.sub(r'[*_`~#>\\-]', '', text)
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', clean_text)
        self.answer_helper.speak(clean_text)
        
    # def print_history(self) -> None:
    #     """Print the conversation history with timestamps"""
    #     timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    #     user_prefix = f"{self.user_name}: " if self.user_name else "User: "
    #     print(f"[{timestamp}] {user_prefix}{self.question}")
    #     print(f"[{timestamp}] {self.name}: {self.response}\n")

    # def process_command(self, command: str) -> str:
    #     """
    #     Process a user command and generate a response.
        
    #     Args:
    #         command: The user's command/input
            
    #     Returns:
    #         str: The assistant's response
    #     """
    #     self.question = command
    #     if not command:
    #         return ""

    #     # Try to extract name if we don't have one yet
    #     if not self.user_name:
    #         if self.extract_name_from_response(command):
    #             response = f"Nice to meet you, {self.user_name}!"
    #             self.add_to_history(command, response)
    #             return response

    #     # Check for predefined Q&A
    #     if self.files and hasattr(self.files, 'qa_dictionary') and command in self.files.qa_dictionary:
    #         response = self.files.qa_dictionary[command]
    #         if self.user_name:
    #             response = f"{self.user_name}, {response}"
    #         self.add_to_history(command, response)
    #         return response

    #     # Handle time/date queries
    #     if "time" in command and "date" in command:
    #         response = self.tell_datetime()
    #         self.add_to_history(command, response)
    #         return response
    #     elif "time" in command:
    #         response = self.tell_time()
    #         self.add_to_history(command, response)
    #         return response
    #     elif "date" in command:
    #         response = self.tell_date()
    #         self.add_to_history(command, response)
    #         return response
    #     elif "day" in command:
    #         response = self.tell_day()
    #         self.add_to_history(command, response)
    #         return response

    #     # Handle goodbye/exit commands
    #     if any(word in command for word in ["goodbye", "bye", "exit", "quit", "stop"]):
    #         response = f"Goodbye, {self.user_name}!" if self.user_name else "Goodbye!"
    #         self.add_to_history(command, response)
    #         return response

    #     # Handle name-related queries
    #     if "what" in command and "name" in command:
    #         if self.user_name:
    #             response = f"Your name is {self.user_name}."
    #         else:
    #             response = "I don't know your name yet. What should I call you?"
    #         self.add_to_history(command, response)
    #         return response

    #     # Use AI to respond
    #     response = self._generate_ai_response(command)
        
    #     # Personalize response if we have user's name
    #     if self.user_name and not response.startswith(self.user_name):
    #         response = f"{self.user_name}, {response}"
        
    #     self.response = response
    #     self.add_to_history(command, response)
    #     return response

    # def _generate_ai_response(self, command: str) -> str:
    #     """Generate AI response using available services"""
    #     try:
    #         # Check if we have internet connection and can use online AI
    #         if self.status and hasattr(self.status, 'is_connected') and self.status.is_connected:
    #             # Import here to avoid circular imports
    #             try:
    #                 from .ai_providers.cohere_api import ask_cohere
    #                 return ask_cohere(command)
    #             except ImportError:
    #                 print("Cohere API not available")
            
    #         # Fallback to local AI if available
    #         if self.ollama and hasattr(self.ollama, 'ask_ollama'):
    #             return self.ollama.ask_ollama(command)
                
    #     except Exception as e:
    #         print(f"AI response error: {e}")
        
    #     # Final fallback responses
    #     fallback_responses = {
    #         'hello': "Hello! How can I help you today?",
    #         'how are you': "I'm doing well, thank you for asking!",
    #         'help': "I can help you with questions about time, date, general information, and more!",
    #         'what can you do': "I can answer questions, tell time and date, have conversations, and help with various tasks.",
    #     }
        
    #     command_lower = command.lower()
    #     for key, fallback in fallback_responses.items():
    #         if key in command_lower:
    #             return fallback
        
    #     return "I'm not sure how to respond to that. Could you rephrase your question?"

    # def run(self) -> None:
    #     """Main conversation loop"""
    #     self.set_conversation_state(ConversationState.WAITING)
    #     self.greet()
        
    #     while True:
    #         try:
    #             query = self.listen_with_timeout()
    #             if query:
    #                 response = self.process_command(query)
    #                 if response:
    #                     self.speak(response)
    #             else:
    #                 # No input received within timeout, ask a prompt
    #                 self.ask_next_prompt()
                
    #             time.sleep(1)  # Brief pause between cycles
                
    #         except KeyboardInterrupt:
    #             self.speak("Goodbye!")
    #             break
    #         except Exception as e:
    #             print(f"Error in main loop: {e}")
    #             time.sleep(2)

    # def set_timeout(self, seconds: int) -> None:
    #     """Set the timeout duration in seconds"""
    #     self.timeout_seconds = seconds
    #     print(f"Timeout set to {seconds} seconds")

    # def is_connected(self) -> bool:
    #     """Check if the assistant has internet connectivity"""
    #     return self.status.is_connected if self.status else False

    # def current_response(self):
    #     return self.answer_helper.

# For backward compatibility, create an alias
# Assistant = ConversationalAssistant

def test():
    files = Files()
    answer_helper = AnswerHelper()
    question_helper = QuestionHelper()
    assistant = ConversationalAssistant(
        files=files,
        answer_helper=answer_helper,
        question_helper=question_helper,
        name="Test Assistant"
    )
    assistant.greet()
    while True:
        assistant.listen()
        print(assistant.question)
        print(assistant.question_helper.what_spoken())
        # assistant.answer()
        print("-" * 30)
if __name__ == "__main__":
    test()