# Timeout Assistant Usage Guide

## Overview
The AI Voice Assistant now includes a timeout mechanism that waits for 10 seconds for user input. If no input is received within this time, the assistant will proactively ask prompting questions.

## Key Features

### 1. Timeout Mechanism
- Default timeout: 10 seconds
- Configurable timeout duration
- Automatic fallback to prompting questions

### 2. Conversation State Management
- `waiting`: Assistant is waiting for input
- `listening`: Assistant is actively listening
- `processing`: Assistant is processing the command

### 3. Smart Prompting System
- Asks for user's name first
- Cycles through engaging questions
- Personalizes responses using the user's name

### 4. Name Recognition
- Automatically extracts names from user responses
- Supports multiple name patterns:
  - "My name is John"
  - "I'm Sarah"
  - "Call me Mike"
  - "David is my name"

## Usage Examples

### Basic Usage
```python
from assistant import Assistant
from status import Status
from tts import TTS
from ollama import Ollama
from files import Files

# Initialize components
from src.assistant.assistant import ConversationalAssistant
from src.assistant.status.status import Status
from src.assistant.robot.answer_helper.tts.tts import PIPER_TTS
from src.assistant.ai_providers.ollama import Ollama
from src.assistant.files.files import Files

status = Status()
tts = PIPER_TTS()
ollama = Ollama()
files = Files()

# Create assistant
assistant = ConversationalAssistant(
    name="ARIA",
    voice_config=None,
    status=status,
    tts=tts,
    ollama=ollama,
    files=files
)

# Set custom timeout (optional)
assistant.set_timeout(15)  # 15 seconds

# Start conversation
assistant.greet()
assistant.run()  # Runs with timeout functionality
```

### Manual Control
```python
# Get conversation information
info = assistant.get_conversation_info()
print(f"User: {info['user_name']}")
print(f"State: {info['conversation_state']}")

# Check if waiting for input
if assistant.is_waiting_for_input():
    print("Assistant is waiting for user input...")

# Reset conversation
assistant.reset_conversation()
```

## Configuration Options

### Timeout Settings
```python
# Set timeout duration
assistant.set_timeout(10)  # 10 seconds (default)
assistant.set_timeout(30)  # 30 seconds for slower users
assistant.set_timeout(5)   # 5 seconds for quick interactions
```

### Custom Prompts
You can modify the prompts by updating the `prompts` list in the `__init__` method:

```python
self.prompts = [
    "What's your name?",
    "How are you feeling today?",
    "What would you like to know?",
    # Add your custom prompts here
]
```

## Workflow

1. **Start**: Assistant begins listening with timeout
2. **Listen**: Waits for user input (default 10 seconds)
3. **Process**: If input received, processes the command
4. **Prompt**: If no input, asks a prompting question
5. **Repeat**: Returns to listening state

## Error Handling

The assistant handles various scenarios:
- Speech recognition errors
- Network connectivity issues
- Microphone access problems
- Timeout exceptions

## Testing

Use the provided test script to verify functionality:

```bash
cd /path/to/AI-Voice-Assistant/src
python test_timeout_assistant.py
```

Choose between:
1. Full interactive test with audio
2. Manual command testing without audio

## Integration with Existing Code

The timeout functionality is backward compatible. Existing code using `assistant.run()` will automatically use the new timeout system.

For legacy support, the old `listen()` method now calls `listen_with_timeout()`.
