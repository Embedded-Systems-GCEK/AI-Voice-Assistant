
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
import threading
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class VoiceType(Enum):
    """Enumeration of available voice types"""
    DEFAULT = "default"
    MALE = "male"
    FEMALE = "female"
    ROBOTIC = "robotic"
    NATURAL = "natural"


class Language(Enum):
    """Enumeration of supported languages"""
    ENGLISH_US = "en-US"
    MALAYALAM = "ml-IN"

class ConversationState(Enum):
    """Enumeration of conversation states"""
    WAITING = "waiting"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    IDLE = "idle"


@dataclass
class VoiceConfig:
    """Configuration class for voice settings"""
    voice_type: VoiceType = VoiceType.DEFAULT
    language: Language = Language.ENGLISH_US
    speed: float = 1.0
    pitch: float = 1.0
    volume: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert voice config to dictionary"""
        return {
            'voice_type': self.voice_type.value,
            'language': self.language.value,
            'speed': self.speed,
            'pitch': self.pitch,
            'volume': self.volume
        }


class BARE_ROBO:
    """
    Basic robot class with fundamental properties.

    This is the foundation class that provides basic robot functionality
    like naming and identification.
    """

    def __init__(self, name: str = "Default Robot"):
        self._name = name
        self._id = id(self)  # Unique identifier
        self._is_active = True
        self._created_at = None  # Can be set by subclasses

    @property
    def name(self) -> str:
        """Get the robot's name"""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the robot's name"""
        if not value or not value.strip():
            raise ValueError("Robot name cannot be empty")
        self._name = value.strip()

    @property
    def robot_id(self) -> int:
        """Get the unique robot identifier"""
        return self._id

    @property
    def is_active(self) -> bool:
        """Check if the robot is active"""
        return self._is_active

    def activate(self) -> None:
        """Activate the robot"""
        self._is_active = True

    def deactivate(self) -> None:
        """Deactivate the robot"""
        self._is_active = False

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the robot"""
        return {
            'name': self.name,
            'id': self.robot_id,
            'active': self.is_active,
            'type': self.__class__.__name__
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', id={self.robot_id})"

    def __repr__(self) -> str:
        return self.__str__()


class SPEAKING_ROBOT(BARE_ROBO):
    """
    Speaking robot class with voice capabilities.

    Extends BARE_ROBO with voice synthesis and speech functionality.
    """

    def __init__(self, name: str = "Speaking Robot", voice_config: Optional[VoiceConfig] = None):
        super().__init__(name)
        self.voice_config = voice_config or VoiceConfig()
        self._is_speaking = False
        self._speech_queue = []

    @property
    def voice_type(self) -> VoiceType:
        """Get the current voice type"""
        return self.voice_config.voice_type

    @voice_type.setter
    def voice_type(self, value: VoiceType) -> None:
        """Set the voice type"""
        self.voice_config.voice_type = value

    @property
    def language(self) -> Language:
        """Get the current language"""
        return self.voice_config.language

    @language.setter
    def language(self, value: Language) -> None:
        """Set the language"""
        self.voice_config.language = value

    @property
    def speaking_speed(self) -> float:
        """Get the speaking speed"""
        return self.voice_config.speed

    @speaking_speed.setter
    def speaking_speed(self, value: float) -> None:
        """Set the speaking speed (0.5 to 2.0)"""
        if not 0.1 <= value <= 3.0:
            raise ValueError("Speaking speed must be between 0.1 and 3.0")
        self.voice_config.speed = value

    @property
    def is_speaking(self) -> bool:
        """Check if the robot is currently speaking"""
        return self._is_speaking

    def speak(self, text: str) -> bool:
        """
        Speak the given text.

        Args:
            text: The text to speak

        Returns:
            bool: True if speech was successful, False otherwise
        """
        if not self.is_active:
            print(f"{self.name} is not active and cannot speak")
            return False

        if not text or not text.strip():
            print("Cannot speak empty text")
            return False

        try:
            self._is_speaking = True
            print(f"[{self.name}] Speaking: {text}")
            # Here you would integrate with actual TTS engine
            # For now, we'll just simulate speaking
            self._perform_speech(text)
            self._is_speaking = False
            return True
        except Exception as e:
            print(f"Speech error: {e}")
            self._is_speaking = False
            return False

    def _perform_speech(self, text: str) -> None:
        """
        Internal method to perform the actual speech synthesis.
        Override this in subclasses for specific TTS implementations.
        """
        # Default implementation - override in subclasses
        pass

    def stop_speaking(self) -> None:
        """Stop current speech"""
        self._is_speaking = False
        print(f"{self.name} stopped speaking")

    def get_voice_config(self) -> Dict[str, Any]:
        """Get the current voice configuration"""
        return self.voice_config.to_dict()

    def set_voice_config(self, config: VoiceConfig) -> None:
        """Set the voice configuration"""
        self.voice_config = config

    def get_status(self) -> Dict[str, Any]:
        """Get the current status including voice information"""
        status = super().get_status()
        status.update({
            'voice_config': self.get_voice_config(),
            'speaking': self.is_speaking,
            'speech_queue_size': len(self._speech_queue)
        })
        return status


class ASSISTANT(abc.ABC, SPEAKING_ROBOT):
    """
    Abstract base class for AI assistants.

    This class defines the interface that all AI assistants must implement.
    It combines speaking capabilities with listening and intelligent response features.
    """

    def __init__(self, name: str = "AI Assistant", voice_config: Optional[VoiceConfig] = None):
        super().__init__(name, voice_config)
        self._conversation_history = []
        self._listening_mode = False
        self._wake_word = "hey assistant"
        self._conversation_state = ConversationState.IDLE
        self._user_name = ""
        self._timeout_seconds = 10

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
