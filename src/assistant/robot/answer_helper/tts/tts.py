
from enum import Enum
from abc import ABC, abstractmethod
    
    
class TTSState(Enum):
    """When Doing Nothin"""
    IDLE = "idle"
    PROCESSING = "processing"
    """When Speaking"""
    SPEAKING = "speaking"
    """When Something is Wrong"""
    ERROR = "Error"
    
    

class TTS(ABC):
    def __init__(self):
        self._text = ""
        self._state = TTSState.IDLE
        self.id = id(self)
    @abstractmethod
    def speak(self,text: str) -> None:
        """Abstract method to perform text-to-speech synthesis"""
        self.text = text
        self._state = TTSState.PROCESSING

    @property
    def text(self) -> str:
        return self._text
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
    # The 'text' property and abstractmethod for 'text' are contradictory.
    # A TTS class typically takes text as an argument to 'speak', not as a property.
    # Removing the 'text' abstractmethod and property as they don't fit the TTS interface.
    @property
    def state(self) -> TTSState:
        return self._state
    @state.setter
    def state(self, new_state: TTSState):
        self._state = new_state
    def __str__(self) -> str:
        return f"TTS(id={self.id}, text='{self.text}')"
    

