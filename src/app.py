
import json
from assistant import Assistant
from cohere_api import ask_cohere
from ollama import ask_ollama
import urllib.request

def is_connected():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        return True
    except:
        return False


with open("dictionaries.json", "r") as file:
    qa_dictionary = json.load(file)

def process_command(query):
    if query == "":
        return


    if query in qa_dictionary:
        assistant.speak(qa_dictionary[query])
        return

    if "time" in query and "date" in query:
        assistant.tell_datetime()
        return
    elif "time" in query:
        assistant.tell_time()
        return
    elif "date" in query:
        assistant.tell_date()
        return
    elif "day" in query:
        assistant.tell_day()
        return

    if is_connected():
        assistant.speak("Checking with Cohere...")
        response = ask_cohere(query)
    else:
        assistant.speak("I'm offline. Thinking locally...")
        response = ask_ollama(query)

    assistant.speak(response)

def main():
    global assistant
    assistant = Assistant("Cyrus")

    assistant.greet()
    while True:
        query = assistant.listen()
        process_command(query)

if __name__ == "__main__":
    main()
