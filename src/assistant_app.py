
from assistant.assistant import ConversationalAssistant
from assistant.status.status import Status
from assistant.robot.answer_helper.tts.tts import PIPER_TTS
from assistant.ai_providers.ollama import Ollama
from assistant.files.files import Files
from src.assistant.robot.assistant_robo import VoiceConfig
from assistant.robot.answer_helper import AnswerHelper


def main():
    # Initialize all required dependencies
    status = Status()
    tts = PIPER_TTS()  
    ollama = Ollama()
    files = Files()
    voice_config = VoiceConfig(voice="piper", language="en-US")
    answer_helper = AnswerHelper()

    # Create the assistant with all dependencies
    assistant = ConversationalAssistant(
        status=status,
        tts=tts,
        ai_provider=ollama,
        files=files,
        voice_config=voice_config,
        answer_helper=answer_helper,
        name="Cyrus",
    )
    
    # Start the assistant
    try:
        assistant.run()  # This will start the full conversation loop
    except KeyboardInterrupt:
        print("Goodbye!")

if __name__ == "__main__":
    main()

