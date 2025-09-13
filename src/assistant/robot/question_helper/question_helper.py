
from stt.stt import STT
from stt.google_stt import GoogleSTT
from enum import Enum

class QuestionHelperState(Enum):
    """ When Doing Nothing"""
    IDLE = "idle"
    """ When the robot is actively listening for questions"""
    LISTENING = "listening"
    """ When the robot is processing a question"""
    # but this is handled by stt
    # PROCESSING = "processing"
    """ When Something is Wrong"""
    ERROR = "error"

class QuestionHelper:
    """_summary_
 
    _description_   
    Helper class to manage answers and integrate TTS functionality.
    """
    def __init__(self,stt: STT = GoogleSTT()):
        self._state = QuestionHelperState.IDLE
        self._question = ""
        
        """_summary_
        tts is PIPER_TTS by default
        """
        self._stt = stt
    
    
    @property
    def stt(self) -> STT:
        return self._stt
    @stt.setter
    def stt(self, stt: STT):
        self._stt = stt

    
    def hear(self) -> str:
        self.state = QuestionHelperState.LISTENING
        spoken_words = self._stt.hear()
        self.state = QuestionHelperState.IDLE
        return spoken_words
    
    @property
    def state(self) -> QuestionHelperState:
        return self._state
    @state.setter
    def state(self, new_state: QuestionHelperState):
        self._state = new_state
    
    @property
    def question(self) -> str:
        return self._question
    @question.setter
    def question(self, value: str):
        self._question = value

    def what_spoken(self) -> str:
        return self.question
    
    def is_listening(self) -> bool:
        return self.state == QuestionHelperState.LISTENING 
    def is_idle(self) -> bool:
        return self.state == QuestionHelperState.IDLE
    def is_processing(self) -> bool:
        return self.stt.is_processing()