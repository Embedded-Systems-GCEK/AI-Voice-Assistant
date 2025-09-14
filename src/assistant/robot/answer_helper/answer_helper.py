# from answer_helper import TTS
from .tts.tts import TTS
from .tts.piper_tts import PIPER_TTS
from enum import Enum
import threading
# For Test
import time
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
        threading.Thread(target=self.update_state, daemon=True).start()
    
    def update_state(self) -> None:
        while self.tts.is_speaking():
            time.sleep(.01)
            if self.tts.is_speaking():
                self.state = AnswerHelperState.PROCESSING
            else:
                self.state = AnswerHelperState.IDLE
        
        
    def is_speaking(self) -> bool:
        return self.state == AnswerHelperState.PROCESSING or self.tts.is_speaking()
    
def test_answer_helper():
    answer_helper = AnswerHelper()
    answer_helper.speak("Hello, this is a test of the AnswerHelper class.")
    while answer_helper.is_speaking():
        print(answer_helper.state)
        time.sleep(1)
        
    print("Test finished.")

if __name__ == "__main__":
    test_answer_helper()
    