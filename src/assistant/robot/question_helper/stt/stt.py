import abc


class STT(abc.ABC):
    @abc.abstractmethod
    def hear(self) -> str:
        pass
    
import speech_recognition as sr




class GoogleSTT(STT):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.state = "idle"  # listening, processing, idle
    def hear(self) -> str:
        
        # Change state to listening
        self.state = "listening"
        try:
            with sr.Microphone() as source:
                self.recognizer.pause_threshold = 0.5
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=self.timeout_seconds, phrase_time_limit=6)
            
            try:
                command = self.recognizer.recognize_google(audio, language='en-US')
                print(f"You said: {command}")
                self.conversation_state = "processing"
                return command.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return ""
            except sr.RequestError:
                self.speak("Speech service is unavailable.")
                return ""
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            self.conversation_state = "waiting"
            return ""
        except Exception as e:
            print(f"Error during listening: {e}")
            return ""
        
        
        # Placeholder implementation
        # Change state back to idle.
        self.state = "idle"
        
        return what_i_heard
    
    

    
    @property
    def state(self) -> str:
        return self._state
    @state.setter
    def state(self, value: str) -> None:
        self._state = value