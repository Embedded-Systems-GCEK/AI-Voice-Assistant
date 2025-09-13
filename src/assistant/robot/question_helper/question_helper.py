
from .stt.stt import STT

class QustionHelper:
    """_summary_
 
    _description_   
    Helper class to manage answers and integrate TTS functionality.
    """
    def __init__(self):
        self.id = id(self)
        self._answer = ""
        """_summary_
        tts is PIPER_TTS by default
        """
        self._tts = PIPER_TTS()
        self._answer = ""
    
    @property
    def tts(self) -> TTS:
        return self._tts
    @tts.setter
    def tts(self, tts: TTS):
        self._tts = tts
        
    def speak(self, text: str):
        self._tts.text = text
        # change this to a single value , var , like response or something.
        self.answer = text
        self._tts.speak()

    @property
    def answer(self) -> str:
        return self._answer
    @answer.setter
    def answer(self, value: str):
        self._answer = value
    
        