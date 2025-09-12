
from assistant.assistant import ConversationalAssistant
from assistant.status.status import Status
from assistant.robot.answer_helper.tts.tts import PIPER_TTS
from assistant.ai_providers.ollama import Ollama
from assistant.files.files import Files

def main():
    # Initialize all required dependencies
    status = Status()
    tts = PIPER_TTS()  
    ollama = Ollama()
    files = Files()
    
    # Create the assistant with all dependencies
    assistant = ConversationalAssistant(
        name="Cyrus",
        status=status,
        tts=tts,
        ollama=ollama,
        files=files
    )
    
    # Start the assistant
    try:
        assistant.run()  # This will start the full conversation loop
    except KeyboardInterrupt:
        print("Goodbye!")

if __name__ == "__main__":
    main()

