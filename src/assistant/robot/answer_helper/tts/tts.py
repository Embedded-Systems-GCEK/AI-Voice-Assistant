
from enum import Enum
from abc import ABC, abstractmethod
    
    
class TTSState(Enum):
    """Represents the state of the TTS engine.

    IDLE: When doing nothing.
    PROCESSING: When processing text.
    SPEAKING: When speaking (currently not used).
    ERROR: When something is wrong (not implemented).
    """
    IDLE = "idle"
    PROCESSING = "processing"
    # SPEAKING = "speaking"  # Uncomment if/when speaking state is needed
    

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
    
    def is_speaking(self) -> bool:
        return self.state == TTSState.PROCESSING

    
    def done_speaking(self) -> None:
        self.state = TTSState.IDLE