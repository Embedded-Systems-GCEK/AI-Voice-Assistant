from typing import  Dict, Any
from dataclasses import dataclass
from enum import Enum

# Custom Imports
try:
    from .bare_robo import BARE_ROBO
    from .answer_helper.answer_helper import AnswerHelper    
    from .question_helper.question_helper import QuestionHelper
except ImportError:
    from bare_robo import BARE_ROBO
    from answer_helper.answer_helper import AnswerHelper
    from question_helper.question_helper import QuestionHelper

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
                 answer_helper: AnswerHelper = AnswerHelper() ,
                 question_helper: QuestionHelper = QuestionHelper(),
                 voice_config: VoiceConfig = VoiceConfig(), # Use Default Config
                 name: str = "Speaking Robot",
                 ):
        super().__init__(name)
        self._state = TalkingRoboState.INITIALIZED
        self.question = ""
        self.voice_config = voice_config 
        self.answer_helper = answer_helper
        self.question_helper = question_helper 


    def update_state(self):
        """Update the status of the robot"""
        """TODO: If this only have to do it while speaking."""
        while self.answer_helper.is_answering():
            if self.answer_helper.is_answering():
                self.state = TalkingRoboState.SPEAKING
            else:
                self.state = TalkingRoboState.IDLE
    def listen(self):   
        self.state = TalkingRoboState.LISTENING
        """Listen for user input with timeout"""
        self.question_helper.hear()
        self.question = self.question_helper.question
     
    def speak(self,string: str = "") -> None:
        """Talking Robot Has no processing capability"""
        """So it speaks the same"""
        self.state = TalkingRoboState.SPEAKING
        print(f"{self.name} is {self.state.value}")
        self.answer = string if string else self.question
        try:
            self._perform_speech()
            threading.Thread(target=self.update_state, daemon=True).start()
            self.state = TalkingRoboState.IDLE
        except Exception as e:
            print(f"Error during speaking: {e}")
            self.state = TalkingRoboState.ERROR
        

    def _perform_speech(self) -> None:
        """
        Internal method to perform the actual speech synthesis.
        Override this in subclasses for specific TTS implementations.
        """
        self.answer_helper.speak(self.answer)

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
        })
        return status
    @property
    def robot_state(self) -> TalkingRoboState:
        if self._state == TalkingRoboState.SPEAKING and self.answer_helper.is_answering():
            return TalkingRoboState.SPEAKING
        return self._state
    @robot_state.setter
    def robot_state(self, value: TalkingRoboState) -> None:
        self._state = value
    
    @property
    def get_speaking_thread(self) -> threading.Thread | None:
        return self.answer_helper.tts.thread
    
    @property
    def question(self) -> str:
        return self._question
    @question.setter
    def question(self, value: str) -> None:
        self._question = value
              


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
        return self.answer_helper.is_answering()


def test_talking_robot():
    answer_helper = AnswerHelper()
    question_helper = QuestionHelper()
    voice_config = VoiceConfig()
    robot = SPEAKING_ROBOT(
        voice_config=voice_config,
        answer_helper=answer_helper,
        question_helper=question_helper,
        name="Test Robot")
    # robot.listen()
    """Simulate a question"""
    robot.question = "Hello, how are you?"
    print(f"Heard: {robot.question}")
    robot.question = f"Heard you say: {robot.question}"
    robot.speak()
    if robot.get_speaking_thread:
        robot.get_speaking_thread.join()  # Wait for speaking to finish
    
    print(f"{robot.name} is {robot.state.value}")
    
    

if __name__ == "__main__":
    test_talking_robot()