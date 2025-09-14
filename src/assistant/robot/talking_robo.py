from typing import  Dict, Any
from dataclasses import dataclass
from enum import Enum

# Custom Imports
from .bare_robo import BARE_ROBO
from .answer_helper.answer_helper import AnswerHelper    
from .question_helper.question_helper import QuestionHelper

import threading, time
class VoiceType(Enum):
    """Enumeration of available voice types"""
    DEFAULT = "default"
    MALE = "male"
    FEMALE = "female"
    ROBOTIC = "robotic"
    NATURAL = "natural"



class TalkingRoboState(Enum):
    """Enumeration of conversation states"""
    """ When the robot is first initialized """
    INITIALIZED = "initialized"
    """ When the robot is waiting for user input """
    WAITING = "waiting"
    """ When the robot is actively listening """
    LISTENING = "listening"
    """ When the robot is speaking """
    SPEAKING = "speaking"
    """ When the robot is idle """
    IDLE = "idle"
    ERROR = "error"




class Language(Enum):
    """Enumeration of supported languages"""
    ENGLISH_US = "en-US"
    MALAYALAM = "ml-IN"

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

class SPEAKING_ROBOT(BARE_ROBO):
    """
    Speaking robot class with voice capabilities.

    Extends BARE_ROBO with voice synthesis and speech functionality.
    """

    def __init__(self,
                 voice_config: VoiceConfig,
                 answer_helper: AnswerHelper ,
                 question_helper: QuestionHelper,
                 name: str = "Speaking Robot",
                 ):
        super().__init__(name)
        self.state = TalkingRoboState.INITIALIZED
        self._is_speaking = False
        self.voice_config = voice_config 
        self._speech_queue = []
        self.answer_helper = answer_helper
        self.question_helper = question_helper 


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
        return self.answer_helper.tts.is_speaking()


    def update_state(self):
        """Update the status of the robot"""
        while self.answer_helper.is_speaking():
            if self.answer_helper.is_speaking():
                self.state = ConversationState.SPEAKING
            else:
                self.state = ConversationState.IDLE
    def listen(self):   
        self.state = TalkingRoboState.LISTENING
        """Listen for user input with timeout"""
        self.question_helper.hear()
     
    def speak(self, text: str):
        try:
            self._perform_speech(text)
            threading.Thread(target=self.update_state, daemon=True).start()
        except Exception as e:
            print(f"Error during speaking: {e}")
            self.state = ConversationState.ERROR

    def _perform_speech(self, text: str) -> None:
        """
        Internal method to perform the actual speech synthesis.
        Override this in subclasses for specific TTS implementations.
        """
        self.answer_helper.speak(text)

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
    @property
    def state(self) -> TalkingRoboState:
        if self._state == TalkingRoboState.SPEAKING and self.answer_helper.tts.state == TTSState.SPEAKING:
            return TalkingRoboState.SPEAKING
        return self._state
    @state.setter
    def state(self, value: TalkingRoboState) -> None:
        print(f"Talking Robo State {self.state}")
        self._state = value
        

def test_talking_robot():
    answer_helper = AnswerHelper()
    question_helper = QuestionHelper()
    voice_config = VoiceConfig()
    robot = SPEAKING_ROBOT(
        voice_config,
        answer_helper,
        question_helper,
        name="Test Robot")
    robot.speak("Hello, I am your speaking robot.")
    print(robot.get_status())


if __name__ == "__main__":
    test_talking_robot()