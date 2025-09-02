
import speech_recognition as sr

from ollama import ask_ollama
import json
from assistant import Assistant


# Open Dictionary for quick Q&A
with open("dictionaries.json", "r") as file:
    qa_dictionary = json.load(file)

def process_command(query):
    if query == "":
        return
    # === Dictionary Check First ===
    if query in qa_dictionary:
        assistant.speak(qa_dictionary[query])
        return
    else:
        assistant.speak("Let me think about that.")
        response = ask_ollama(query)
        assistant.speak(response)
def main():
    global assistant
    assistant.greet()
    while True:
        query = assistant.listen()
        process_command(query)

if __name__ == "__main__":
    assistant = Assistant("CYRUS")
    main()
