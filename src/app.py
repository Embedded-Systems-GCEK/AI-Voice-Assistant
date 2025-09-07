from assistant import Assistant
from ollama import Ollama
from status import Status
from tts import TTS
from files import Files

def main():
    global assistant
    status = Status()
    ollama = Ollama()
    tts = TTS()
    files = Files()
    assistant = Assistant(status=status, tts=tts, name="Cyrus", ollama=ollama, files=files)
    assistant.greet()
    try:
        while True:
            assistant.run()
    except KeyboardInterrupt:
        print("Exiting...")
        assistant.status.connected = False
if __name__ == "__main__":
    main()