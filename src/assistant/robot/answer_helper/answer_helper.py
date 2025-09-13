
from tts.tts import TTS, TTSState
from tts.piper_tts import PIPER_TTS
from enum import Enum

class AnswerHelperState(Enum):
    """ When Doing Nothing"""
    IDLE = "idle"
    """ When the robot is processing a question"""
    PROCESSING = "processing"
    
    """TODO: SPEAKING is done by the speaker , so seperate that concern from here"""
        
    """ When Something is Wrong"""
    ERROR = "error"
    
class AnswerHelper:
    """_summary_
 
    _description_   
    Helper class to manage answers and integrate TTS functionality.
    """
    def __init__(self,tts: TTS = PIPER_TTS()):
        # super().__init__()
        """_summary_
        tts is PIPER_TTS by default
        """
        self._state = AnswerHelperState.IDLE
        self._tts = tts
    
    @property
    def tts(self) -> TTS:
        return self._tts
    @tts.setter
    def tts(self, tts: TTS):
        self._tts = tts
    
    @property
    def state(self) -> AnswerHelperState:
        return self._state
    @state.setter
    def state(self, new_state: AnswerHelperState):
        self._state = new_state
    
    def speak(self, text: str):
        self.state = AnswerHelperState.PROCESSING
        """Set the text to be spoken and invoke the TTS engine."""
        # change this to a single value , var , like response or something.
        self._tts.speak(text)
        self.state = AnswerHelperState.IDLE
        
    def is_speaking(self) -> bool:
        return self.state == AnswerHelperState.PROCESSING 