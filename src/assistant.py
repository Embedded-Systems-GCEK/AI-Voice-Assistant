import speech_recognition as sr
from tts import get_text, play_audio, save_to_file
import datetime
import re
class Assistant:
    def __init__(self, name: str):
        self.name = name
    def greet(self):
        greeting = f"Hello, I am {self.name}. How can I assist you today?"
        self.speak(greeting)
    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.pause_threshold = 0.5
            audio = recognizer.listen(source, phrase_time_limit=4) 
        try:
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            self.speak("Speech service is unavailable.")
            return ""
        
    def speak(self,text):
        # Remove unwanted characters
        clean_text = re.sub(r'[*_`~#>\\-]', '', text)
        # remove Emojis
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', clean_text)
        # Break long text into 2-4 sentence chunks max
        sentences = [s.strip() for s in clean_text.replace('\n', ' ').split('.') if s.strip()]
        max_sentences = 4
        
        output_chunks = []
        chunk = []
        for sentence in sentences:
            chunk.append(sentence)
            if len(chunk) == max_sentences:
                output_chunks.append('. '.join(chunk) + '.')
                chunk = []
        if chunk:
            output_chunks.append('. '.join(chunk) + '.')

        for chunk_text in output_chunks:
            print(f"Cyrus: {chunk_text}")
            # Send to Piper HTTP API
            try:
                response = get_text(chunk_text)
                if response.ok:
                    save_to_file(response)
                    play_audio()
                else:
                    print("Piper error:", response.text)
            except Exception as e:
                print("Piper request failed:", e)
    def tell_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {now}")
