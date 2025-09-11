from datetime import datetime
import sys
import os

# Add parent directory to path to import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from assistant.assistant import ConversationalAssistant
    from assistant.status.status import Status
    from assistant.robot.answer_helper.tts.tts import PIPER_TTS
    from assistant.ai_providers.ollama import Ollama
    from assistant.files.files import Files
    ASSISTANT_AVAILABLE = True
except ImportError:
    ASSISTANT_AVAILABLE = False
    print("Assistant modules not available")

# Example questions for the Flutter app
EXAMPLE_QUESTIONS = [
    {
        "id": 1,
        "category": "General",
        "question": "What time is it?",
        "description": "Ask for the current time"
    },
    {
        "id": 2,
        "category": "General",
        "question": "What's the date today?",
        "description": "Ask for today's date"
    },
    {
        "id": 3,
        "category": "General",
        "question": "What day is it?",
        "description": "Ask for the current day of the week"
    },
    {
        "id": 4,
        "category": "Personal",
        "question": "How are you?",
        "description": "General greeting and wellbeing check"
    },
    {
        "id": 5,
        "category": "Knowledge",
        "question": "Tell me about artificial intelligence",
        "description": "Learn about AI concepts"
    },
    {
        "id": 6,
        "category": "Knowledge",
        "question": "What is machine learning?",
        "description": "Understand machine learning basics"
    },
    {
        "id": 7,
        "category": "Weather",
        "question": "What's the weather like?",
        "description": "Ask about current weather conditions"
    },
    {
        "id": 8,
        "category": "Personal",
        "question": "What's your name?",
        "description": "Ask the assistant's name"
    },
    {
        "id": 9,
        "category": "Help",
        "question": "What can you help me with?",
        "description": "Learn about assistant capabilities"
    },
    {
        "id": 10,
        "category": "Technology",
        "question": "Explain quantum computing",
        "description": "Learn about quantum computing"
    }
]

# Initialize assistant (if available)
assistant_instance = None
if ASSISTANT_AVAILABLE:
    try:
        status = Status()
        tts = PIPER_TTS()
        ollama = Ollama()
        files = Files()
        assistant_instance = ConversationalAssistant(
            name="ARIA", 
            status=status, 
            tts=tts, 
            ollama=ollama, 
            files=files
        )
        assistant_instance.set_timeout(10)
        print("Assistant initialized successfully")
    except Exception as e:
        print(f"Failed to initialize assistant: {e}")
        ASSISTANT_AVAILABLE = False
