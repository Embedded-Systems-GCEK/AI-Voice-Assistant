import speech_recognition as sr
from speech_recognition.recognizers.google import Alternative
# Custom Imports
from stt import STT, STTState , ConversationState


class GoogleSTT(STT):
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        """ Current state of the STT system """
        self.timeout_seconds = 5  # Default timeout for listening
        """ Current conversation state """
        # Duration to adjust for ambient noise , must be greater than 0.5
        # Type is infered as int for the method , fix it later , {contribute}
        self.adjust_for_ambient_noise_duration = 0.5
        self.recognizer_pause_threshold = 0.5

    @property
    def name(self) -> str:
        return "Google Speech-to-Text"
    def hear(self) -> str:
        super().hear()
        # Change state to listening
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.conversation_state = ConversationState.LISTENING
                self.recognizer.adjust_for_ambient_noise(source, duration=self.adjust_for_ambient_noise_duration)
                self.recognizer.pause_threshold = self.recognizer_pause_threshold
                print("🎤 Listening... (speak now)")
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=self.timeout_seconds, phrase_time_limit=6)

            try:
                # Use Google's speech recognition
                """TODO: Fix this : Attribute "recognize_legacy" is unknown"""
                command = self.recognizer.recognize_google(audio, language='en-US')
                print(f"✅ You said: {command}")
                self.conversation_state = ConversationState.PROCESSING
                self._state = STTState.PROCESSING
                return command.lower()
            except sr.UnknownValueError:
                print("❌ Sorry, I didn't catch that. Could you repeat?")
                self._state = STTState.ERR
                return ""
            except sr.RequestError as e:
                print(f"❌ Speech service error: {e}")
                self._state = STTState.ERR
                return ""

        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout period")
            self.conversation_state = ConversationState.WAITING
            self._state = STTState.IDLE
            return ""
        except Exception as e:
            print(f"❌ Error during listening: {e}")

            self._state = STTState.ERR
            return ""


if __name__ == "__main__":
    # Test the GoogleSTT class
    stt = GoogleSTT()
    print("✅ GoogleSTT class initialized successfully!\n\n")
    while True:
        text = stt.hear()
        if text:
            print(f"Recognized Text: {text}")
        else:
            print("No valid speech recognized.")
            
        print(stt)
        print("-" * 30)
