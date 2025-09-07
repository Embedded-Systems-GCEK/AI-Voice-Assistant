# 🎙️ AI Voice Assistant (Cyrus)

A simple Python voice assistant that c### 5. If `test.wav` plays correctly, TTS is worki### 7. Run the assistant
```bash
python src/app.py
```

You should see:
```
Listening...
```

Now speak into your microphone 🎤.

## 🔎 Features

- **"What's the time/date/day?"** → tells current info
- **"hello" / "who are you"** → answers from dictionary
- **Other questions** → answered by Cohere AI (if online) or Ollama (if offline)
- **Voice responses** → speaks responses with Piper TTSCohere (Optional)

If you want smarter AI replies (when online):

1. Get a free API key from [Cohere](https://cohere.com)
2. Open `src/cohere_api.py`
3. Add your key:

```python
COHERE_API_KEY = "your_api_key_here"
```

> **Note**: If you don't set this, the assistant will fallback to offline Ollama responses.ional)

If you want smarter AI replies (when online):

1. Get a free API key from [Cohere](https://cohere.com)
2. Open `src/cohere_api.py`
3. Add your key:

```python
COHERE_API_KEY = "your_api_key_here"
```

> **Note**: If you don't set this, the assistant will fallback to offline Ollama responses.sten to your voice (SpeechRecognition + Google API)
- 🗣️ Speak back using Piper TTS
- 📅 Tell time, date, day
- 🤖 Answer questions using Cohere AI (when online) or Ollama (offline)
- 📖 Reply with custom answers from dictionaries.json

> **Note**: Install Ollama for offline responses

## ⚡ Quick Setupssistant (Cyrus)

A simple Python voice assistant that can:

🎤 Listen to your voice (SpeechRecognition + Google API)

🗣️ Speak back using Piper TTS

📅 Tell time, date, day

🤖 Answer questions using Cohere AI (when online) or Ollama (offline)

📖 Reply with custom answers from dictionaries a.json
INSTALL OLLAMA FOR OFFFLINE RESPONSES
⚡ Quick Setup
### 1. Clone this repository
```bash
git clone https://github.com/Embedded-Systems-GCEK/AI-Voice-Assistant.git
cd AI-Voice-Assistant
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Piper TTS

1. Download Piper from: [Piper Releases](https://github.com/rhasspy/piper/releases)

2. Place it in a folder called `piper/` at the project root:

```
AI-Voice-Assistant/
├── piper/
│   ├── piper.exe            # (Windows) OR piper (Linux/Mac)
│   ├── en_US-amy-low.onnx
│   └── en_US-amy-low.onnx.json
```

3. Test Piper manually:
```bash
echo Hello world | ./piper/piper.exe --model ./piper/en_US-amy-low.onnx --output_file test.wav
```

If `test.wav` plays correctly, TTS is working.


5. Setup Cohere (Optional)

If you want smarter AI replies (when online):

Get a free API key from Cohere

Open src/cohere_api.py

Add your key:

COHERE_API_KEY = "your_api_key_here"


(If you don’t set this, the assistant will fallback to offline Ollama responses.)

### 6. Check dictionaries.json

Make sure `dictionaries.json` exists in the project root. Example:

```json
{
  "hello": "Hi there! How can I help you?",
  "who are you": "I am Cyrus, your personal assistant."
}
```

7. Run the assistant
python src/app.py


You should see:

Listening...


Now speak into your microphone 🎤.

🔎 Features

"What’s the time/date/day?" → tells current info

"hello" / "who are you" → answers from dictionary

Other questions → answered by Cohere AI (if online) or Ollama (if offline)

Speaks responses with Piper TTS

## ❓ Troubleshooting

**`dictionaries.json` not found** → Make sure the file is in repo root.

**Piper errors** → Check that `piper.exe` and `en_US-amy-low.onnx` are inside `piper/`.

**Microphone not working** → Install PyAudio properly. On Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

**Cohere errors** → Check your API key.