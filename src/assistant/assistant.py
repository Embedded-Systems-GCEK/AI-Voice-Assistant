"""
Assistant Module

This module contains the concrete implementation of the ConversationalAssistant class.
It provides a complete conversational AI assistant with speech recognition,
response generation, and conversation management.
"""

import re
from enum import Enum 

from .ai_provider import AIProvider, Ollama
from .robot.assistant_robo import ASSISTANT
from .files.files import Files


class AsistantStatusErr(Enum):
    FILE = "path not found"
    NET = "network error"
    AUTH = "authentication error"
    ERR = "general error"
    NONE = "no error"
class AssistantStatus(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    READY = "ready"
    ERROR = AsistantStatusErr


class ConversationStates(Enum):
    """Enumeration of conversation states"""
    """ When the robot is first initialized """
    INITIALIZED = "initialized"
    """ When the robot is waiting for user input """
    IDLE = "idle"
    """ When the robot is actively listening for user input """
    LISTENING = "listening"
    """ When the robot is processing user input """
    PROCESSING = "processing"
    """ When the robot is responding to user input """
    RESPONDING = "responding"
    """ When the robot encounters an error """
    ERROR = "error"


class ConversationalAssistant(ASSISTANT):
    """
    Concrete implementation of an AI assistant with full conversation capabilities.
    This class implements all the abstract methods from ASSISTANT and provides
    a complete conversational AI assistant with speech recognition, response generation,
    and conversation management.
    """

    def __init__(self, 
                ai_provider: AIProvider,
                name: str = "Conversational Assistant",
                ):
        super().__init__(
            name=name,
        )
        """Files Object for File Operations"""
        self.file = Files()
        """Only Conversational Assistant Returns Something"""
        self.response = ""

        self.current_prompt_index = 0
        self._state = ConversationStates.INITIALIZED
        self._ai_provider = ai_provider

    @property
    def ai_provider(self) -> AIProvider:
        return self._ai_provider

    @ai_provider.setter
    def ai_provider(self, provider: AIProvider):
        self._ai_provider = provider

    def greet(self) -> None:
        """Perform a greeting sequence"""
        greeting = f"Hello, I am {self.name}. How can I assist you today?"
        self.response = greeting
        self.speak(greeting)

    def answer(self, text: str = "") -> None:
        """
        Speak the given text and manage conversation history.

        Args:
            text: The text to speak

        Returns:
            bool: True if speech was successful, False otherwise
        """
        """Process Command First"""
        self.process_command()

        text = self.response if not text else text
        # Clean unwanted characters
        clean_text = re.sub(r"[*_`~#>\\-]", "", text)
        clean_text = re.sub(r"[\U00010000-\U0010ffff]", "", clean_text)
        self.answer_helper.speak(clean_text)

    def process_command(self, cmd: str = "") -> None:
        """First set the state to processing"""
        super().process_command()
        self.state = ConversationStates.PROCESSING
        """Get the question
        Multiple methods available 
        question = self.question_helper.question
        question = self.question_helper.stt.text
        question = self.question_helper.what_spoken()
        """
        self.query = cmd if cmd else self.question_helper.question
        question = self.question_helper.what_spoken()
        try:
            self.response = self.ask_to_ai(question)
        except Exception as e:
            print(f"Error in process_command: {e}")
            self.state = ConversationStates.ERROR
        """Now Speak The Response"""

    def ask_to_ai(self, question: str) -> str:
        response = self.ai_provider.ask(question)
        return response

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: ConversationStates):
        self._state = new_state

    @property
    def response(self) -> str:
        return self._response

    @response.setter
    def response(self, value: str):
        self._response = value

    def is_answering(self) -> bool:
        _is_answering = self.answer_helper.is_answering() or self.state == ConversationStates.PROCESSING
        return _is_answering
            

def test():
    ai_provider = Ollama()  # Replace with a concrete implementation
    assistant = ConversationalAssistant(
        ai_provider=ai_provider,
        name="Test Assistant",
    )

    assistant.process_command("What is 2 + 2?")
    assistant.answer()
    # assistant.answer()
    while assistant.is_answering():
        pass
    print("-" * 30)
