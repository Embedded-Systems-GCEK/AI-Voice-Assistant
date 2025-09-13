
"""
Robot Types Module

This module defines the hierarchical structure of robot types for the AI Voice Assistant.
It provides a clean, extensible architecture for different robot capabilities.

Hierarchy:
- BARE_ROBO: Basic robot with name property
- SPEAKING_ROBOT: Adds voice capabilities
- ASSISTANT: Abstract base for AI assistants with listening capabilities
- ConversationalAssistant: Concrete implementation with conversation management
"""

import abc
import speech_recognition as sr
import datetime
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Custom Imports

from answer_helper.answer_helper import AnswerHelper
from question_helper.question_helper import QuestionHelper
from talking_robo import SPEAKING_ROBOT, VoiceConfig , ConversationState


class ASSISTANT(abc.ABC, SPEAKING_ROBOT):
    """
    Abstract base class for AI assistants.

    This class defines the interface that all AI assistants must implement.
    It combines speaking capabilities with listening and intelligent response features.
    """

    def __init__(self, 
        voice_config: VoiceConfig ,
        answer_helper: AnswerHelper,
        question_helper: QuestionHelper,
        name: str = "AI Assistant",
        ):
        super().__init__(
            name=name,
            voice_config=voice_config,
            answer_helper=answer_helper,
            question_helper=question_helper,
            )
        self.id = id(self) 
        self._conversation_history = []
        self._listening_mode = False
        self._wake_word = "hey assistant"
        self._conversation_state = ConversationState.IDLE
        self._user_name = ""
        self._timeout_seconds = 10

    """
    TODO: Implement this after , v0.1.0 Release.
    """
    
    @property
    def wake_word(self) -> str:
        """Get the wake word for the assistant"""
        return self._wake_word

    @wake_word.setter
    def wake_word(self, value: str) -> None:
        """Set the wake word"""
        self._wake_word = value.lower().strip()

    @property
    def conversation_history(self) -> list:
        """Get the conversation history"""
        return self._conversation_history.copy()

    @property
    def is_listening(self) -> bool:
        """Check if the assistant is currently listening"""
        return self._listening_mode

    @property
    def conversation_state(self) -> ConversationState:
        """Get the current conversation state"""
        return self._conversation_state

    @property
    def user_name(self) -> str:
        """Get the user's name"""
        return self._user_name

    @user_name.setter
    def user_name(self, value: str) -> None:
        """Set the user's name"""
        self._user_name = value.strip().capitalize()

    @property
    def timeout_seconds(self) -> int:
        """Get the timeout duration in seconds"""
        return self._timeout_seconds

    @timeout_seconds.setter
    def timeout_seconds(self, value: int) -> None:
        """Set the timeout duration in seconds"""
        if value < 1:
            raise ValueError("Timeout must be at least 1 second")
        self._timeout_seconds = value

    @abc.abstractmethod
    def listen(self) -> str:
        """
        Listen for user input.

        Returns:
            str: The recognized speech text, or empty string if no speech detected
        """
        pass

    @abc.abstractmethod
    def process_command(self, command: str) -> str:
        """
        Process a user command and generate a response.

        Args:
            command: The user's command/input

        Returns:
            str: The assistant's response
        """
        pass

    @abc.abstractmethod
    def greet(self) -> None:
        """Perform a greeting sequence"""
        pass

    def add_to_history(self, user_input: str, assistant_response: str) -> None:
        """Add an interaction to the conversation history"""
        self._conversation_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'user': user_input,
            'assistant': assistant_response
        })

        # Keep only last 100 interactions
        if len(self._conversation_history) > 100:
            self._conversation_history = self._conversation_history[-100:]

    def clear_history(self) -> None:
        """Clear the conversation history"""
        self._conversation_history.clear()

    def start_listening(self) -> None:
        """Start listening mode"""
        if not self.is_active:
            print(f"{self.name} is not active")
            return
        self._listening_mode = True
        self._conversation_state = ConversationState.LISTENING
        print(f"{self.name} is now listening...")

    def stop_listening(self) -> None:
        """Stop listening mode"""
        self._listening_mode = False
        self._conversation_state = ConversationState.IDLE
        print(f"{self.name} stopped listening")

    def set_conversation_state(self, state: ConversationState) -> None:
        """Set the conversation state"""
        self._conversation_state = state

    def extract_name_from_response(self, query: str) -> bool:
        """Extract name from user response and store it"""
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
                return True
        
        # If no pattern matches but it seems like they're responding to name question
        if not self.user_name and any(word in query for word in ["name", "call", "i'm", "i am"]):
            words = query.split()
            if len(words) > 0:
                potential_name = words[-1].strip('.,!?').capitalize()
                if len(potential_name) > 1 and potential_name.isalpha():
                    self.user_name = potential_name
                    return True
        
        return False

    def tell_time(self) -> str:
        """Get the current time"""
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}"

    def tell_date(self) -> str:
        """Get today's date"""
        today = datetime.datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {today}"

    def tell_day(self) -> str:
        """Get the current day"""
        day = datetime.datetime.now().strftime("%A")
        return f"Today is {day}"

    def tell_datetime(self) -> str:
        """Get the current date and time"""
        dt = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        return f"The current date and time is {dt}"

    def get_conversation_info(self) -> Dict[str, Any]:
        """Get current conversation state information"""
        return {
            "user_name": self.user_name,
            "conversation_state": self.conversation_state.value,
            "timeout_seconds": self.timeout_seconds,
            "assistant_name": self.name,
            "history_count": len(self._conversation_history),
            "is_listening": self.is_listening,
            "is_active": self.is_active
        }

    def reset_conversation(self) -> None:
        """Reset conversation state"""
        self._user_name = ""
        self._conversation_state = ConversationState.WAITING
        self.clear_history()

    def is_waiting_for_input(self) -> bool:
        """Check if assistant is currently waiting for user input"""
        return self._conversation_state == ConversationState.WAITING

    def get_status(self) -> Dict[str, Any]:
        """Get the current status including assistant-specific information"""
        status = super().get_status()
        status.update({
            'listening': self.is_listening,
            'wake_word': self.wake_word,
            'conversation_count': len(self._conversation_history),
            'conversation_state': self.conversation_state.value,
            'user_name': self.user_name,
            'timeout_seconds': self.timeout_seconds
        })
        return status

    
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', listening={self.is_listening}, state={self.conversation_state.value})"
