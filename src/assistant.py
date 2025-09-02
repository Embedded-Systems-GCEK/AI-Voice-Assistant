# assistant.py
import speech_recognition as sr
from tts import speak
import datetime
import re

class Assistant:
    def __init__(self, name: str):
        self.name = name

    def greet(self):
        greeting = f"Hello, I am {self.name}. How can I assist you today?"
        speak(greeting)

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.pause_threshold = 0.5
            audio = recognizer.listen(source, phrase_time_limit=6)
        try:
            command = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable.")
            return ""

    def speak(self, text):
        clean_text = re.sub(r'[*_`~#>\\-]', '', text)
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', clean_text)
        speak(clean_text)

    def tell_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    def tell_date(self):
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    def tell_day(self):
        day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {day}")

    def tell_datetime(self):
        dt = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        speak(f"The current date and time is {dt}")
