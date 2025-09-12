
from tts.tts import PIPER_TTS

class AnswerHelper:
    def __init__(self):
        self.id = id(self)
        self._answer = ""
        self._tts = PIPER_TTS()
        self._answer = ""
        
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
    
        