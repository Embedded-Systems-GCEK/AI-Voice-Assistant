import abc

from enum import Enum

class STTState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    ERR = "error"
class STT(abc.ABC):
    def __init__(self):
        self._state = STTState.IDLE
        self._name = "Abstract STT"
        
    @abc.abstractmethod
    def hear(self) -> str:
        self._state = STTState.LISTENING
        pass
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def state(self) -> STTState:
        return self._state
    @state.setter
    def state(self, new_state: STTState):
        self._state = new_state

    def reset(self) -> None:
        """Reset the STT state to idle"""
        self._state = STTState.IDLE
    

    def is_listening(self) -> bool:
        """Check if currently listening"""
        return self._state == STTState.LISTENING

    def is_processing(self) -> bool:
        """Check if currently processing speech"""
        return self._state == STTState.PROCESSING
    def __str__(self) -> str:
        return f"name={self.name}, state={self.state}"
