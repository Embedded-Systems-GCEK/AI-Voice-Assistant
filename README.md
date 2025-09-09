# 🎙️ AI Voice Assistant (Cyrus)

A simple Python voice assistant that can:

- 🎤 Listen to your voice (SpeechRecognition + Google API)
- 🗣️ Speak back using Piper TTS
- 📅 Tell time, date, day
- 🤖 Answer questions using Cohere AI (when online) or Ollama (offline)
- 📖 Reply with custom answers from dictionaries.json

> **Note**: This project includes a demo mode that works without speech recognition or TTS for testing.

## ⚡ Quick Start

### Option 1: Easy Installation (Recommended)
```bash
git clone https://github.com/Embedded-Systems-GCEK/AI-Voice-Assistant.git
cd AI-Voice-Assistant
python install.py
```

### Option 2: Demo Mode (No Dependencies Required)
```bash
git clone https://github.com/Embedded-Systems-GCEK/AI-Voice-Assistant.git
cd AI-Voice-Assistant
python demo.py
```

### Option 3: Manual Installation

#### 1. Clone this repository
```bash
git clone https://github.com/Embedded-Systems-GCEK/AI-Voice-Assistant.git
cd AI-Voice-Assistant
```

#### 2. Create and activate a virtual environment

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

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup Piper TTS

The project includes Piper TTS files for Windows. For Linux/Mac:

1. Download Piper from: [Piper Releases](https://github.com/rhasspy/piper/releases)
2. Download the appropriate version:
   - Linux x86_64: `piper_linux_x86_64.tar.gz`
   - Linux ARM64: `piper_linux_aarch64.tar.gz`
   - macOS: `piper_macos_x64.tar.gz`
3. Extract to the `piper/` directory
4. Ensure the executable is named `piper` (without .exe extension)

Test Piper manually:
```bash
# Linux/Mac
echo "Hello world" | ./piper/piper --model ./piper/en_US-amy-low.onnx --output_file test.wav

# Windows
echo "Hello world" | ./piper/piper.exe --model ./piper/en_US-amy-low.onnx --output_file test.wav
```

#### 5. Setup Cohere (Optional)

If you want smarter AI replies (when online):

1. Get a free API key from [Cohere](https://cohere.com)
2. Open `src/cohere_api.py`
3. Replace the existing key with your key:

```python
COHERE_API_KEY = "your_api_key_here"
```

> **Note**: If you don't set this, the assistant will fallback to offline Ollama responses.

#### 6. Setup Ollama (Optional, for offline AI)

1. Install [Ollama](https://ollama.ai/)
2. Download a model:
```bash
ollama run mistral:7b
```

## 🚀 Running the Assistant

### Full Voice Assistant (with dependencies)
```bash
python src/app.py
```

### Demo Mode (text-based, no dependencies)
```bash
python demo.py
```

### Using the installation script's run script
```bash
# Linux/Mac
./run_assistant.sh

# Windows
run_assistant.bat
```

## 🧪 Testing Your Setup

Run the setup verification script:
```bash
python test_setup.py
```

This will check:
- ✅ Python version compatibility
- ✅ Required packages installation
- ✅ Piper TTS setup
- ✅ Configuration files
- ✅ Source code integrity

## 🔎 Features

### Built-in Responses
- **"hello"** / **"hi"** / **"hey"** → Greetings
- **"who are you"** / **"what is your name"** → Introduction  
- **"what can you do"** → Capabilities overview
- **"tell me a joke"** → Programming joke

### Time & Date
- **"what time is it"** → Current time
- **"what's the date"** → Current date  
- **"what day is it"** → Current day
- **"time and date"** → Complete date/time info

### APCI 2025 Conference Information
- **"what is apci"** → Conference overview
- **"when is apci 2025"** → Conference dates
- **"where is apci 2025"** → Conference location
- **"what is track X"** → Information about conference tracks (1-10)

### AI-Powered Responses
- **Other questions** → Answered by Cohere AI (if online) or Ollama (if offline)
- **Voice responses** → Speaks responses with Piper TTS

## ❓ Troubleshooting

### Common Issues

**`dictionaries.json` not found**
- Ensure you're running commands from the project root directory

**Piper TTS errors**
- Download the correct Piper version for your operating system
- Ensure executable permissions on Linux/Mac: `chmod +x piper/piper`

**PyAudio installation issues:**

*Windows:*
```bash
pip install pipwin
pipwin install pyaudio
```

*Linux (Ubuntu/Debian):*
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

*macOS:*
```bash
brew install portaudio
pip install pyaudio
```

**Speech recognition not working**
- Check microphone permissions
- Ensure internet connection (uses Google Speech API)

**Cohere API errors**
- Verify your API key in `src/cohere_api.py`
- Check your Cohere API usage limits

**No offline AI responses**
- Install [Ollama](https://ollama.ai/)
- Run: `ollama run mistral:7b`

### Getting Help

1. Run `python test_setup.py` to diagnose issues
2. Check the console output for specific error messages  
3. Try the demo mode first: `python demo.py`

## 🏗️ Project Structure

```
AI-Voice-Assistant/
├── src/
│   ├── app.py           # Main application entry point
│   ├── assistant.py     # Core assistant logic
│   ├── cohere_api.py    # Cohere AI integration
│   ├── files.py         # File handling for dictionaries
│   ├── ollama.py        # Ollama integration for offline AI
│   ├── status.py        # Internet connection status
│   └── tts.py          # Text-to-speech using Piper
├── .github/            # GitHub templates and workflows
│   ├── ISSUE_TEMPLATE/ # Bug reports, feature requests, etc.
│   └── workflows/      # CI/CD automation
├── piper/              # Piper TTS files and models
├── dictionaries.json   # Pre-configured Q&A responses
├── requirements.txt    # Python dependencies
├── install.py         # Automatic installation script
├── demo.py           # Demo mode (no dependencies)
├── test_setup.py     # Setup verification script
├── version.py        # Version management utility
├── VERSION           # Current release version
├── CONTRIBUTING.md   # Team collaboration guidelines
├── CODE_OF_CONDUCT.md # Community standards
└── README.md         # This file
```

## 📊 Version Information

Check the current version and release information:
```bash
python version.py info
```

This will show:
- Current version number
- Git commit hash
- Git branch
- Python version

## 📝 Configuration Files

### dictionaries.json
Contains pre-configured question-answer pairs. You can add your own:

```json
{
  "your question": "Your custom response",
  "another question": "Another response"
}
```

### src/cohere_api.py
Configure your Cohere API key for online AI responses:

```python
COHERE_API_KEY = "your_api_key_here"
```

## 🤝 Contributing

This project is developed by teams at Government College of Engineering Kannur for the APCI 2025 conference. We welcome contributions from all team members!

### Team Structure
- **👨‍💻 Developers:** @Nivedh-r, @dhanashyam18, @AmayaPramod, @AbhayaGovind
- **🧪 Testers:** @Sneha-SJ-05, @MeenakshiPoyyil  
- **🎨 Designers:** @vyshnav8486, @aruncs31s

### Quick Contributing Guide
1. Read our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
2. Check our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards
3. Use our issue templates for bug reports, feature requests, and testing reports
4. Follow the development workflow described in CONTRIBUTING.md

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Run `python test_setup.py` to verify your setup
4. Make your changes following our coding standards
5. Test with both `python demo.py` and full voice mode
6. Submit a pull request with clear description

For detailed team-specific guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

This project is part of the APCI 2025 conference initiative at Government College of Engineering Kannur, Kerala, India.