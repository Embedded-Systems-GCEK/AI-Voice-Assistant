import speech_recognition as sr
from cohere_api import ask_cohere
import datetime
import re
from status import Status
from tts import TTS
from ollama import Ollama
from files import Files
import threading
class Assistant:
    def __init__(self, status: Status, name: str, tts: TTS,ollama: Ollama,files: Files):
        self.status: Status = status
        self.name: str = name
        self.tts: TTS = tts
        self.ollama: Ollama = ollama
        self.files = files
        self.recognizer: sr.Recognizer = sr.Recognizer()
        self.question: str = ""
        self.response: str = ""
    def run(self):
        query: str = self.listen()
        self.process_command(query)
    def is_connected(self) -> bool:
        return self.status.connected
    def greet(self):
        greeting: str = f"Hello, I am {self.name}. How can I assist you today?"
        self.tts.speak(greeting)
    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.pause_threshold = 0.5
            audio = self.recognizer.listen(source, phrase_time_limit=6)
        try:
            command = self.recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            self.speak("Speech service is unavailable.")
            return ""
    def speak(self, text):
        self.response = text
        threading.Thread(target=self.print_history, daemon=True).start()
        # Clean unwanted chars
        clean_text = re.sub(r'[*_`~#>\\-]', '', text)
        clean_text = re.sub(r'[\U00010000-\U0010ffff]', '', clean_text)
        self.tts.speak(clean_text)
    def tell_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {now}")

    def tell_date(self):
        today = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today's date is {today}")
    def tell_day(self):
        day = datetime.datetime.now().strftime("%A")
        self.speak(f"Today is {day}")
    def tell_datetime(self):
        dt = datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        self.speak(f"The current date and time is {dt}")
    def print_history(self):
        print(f"Q: {self.question}\nA: {self.response}\n")
        
    def process_command(self, query: str) -> None:
        self.question = query
        if query == "":
            return
        if query in self.files.qa_dictionary:
            self.speak(self.files.qa_dictionary[query])
            return

        if "time" in query and "date" in query:
            self.tell_datetime()
            return
        elif "time" in query:
            self.tell_time()
            return
        elif "date" in query:
            self.tell_date()
            return
        elif "day" in query:
            self.tell_day()
            return

        if self.status.is_connected:
            self.speak("Checking with Cohere...")
            response = ask_cohere(query)
        else:
            self.speak("I'm offline. Thinking locally...")
            self.response = self.ollama.ask_ollama(query)
        self.speak(self.response)
