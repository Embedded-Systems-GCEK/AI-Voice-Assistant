
import subprocess
import tempfile
import os
import platform
import winsound

from abc import ABC, abstractmethod


class TTS(ABC):
    @abstractmethod
    def speak(self) -> None:
        pass

    # The 'text' property and abstractmethod for 'text' are contradictory.
    # A TTS class typically takes text as an argument to 'speak', not as a property.
    # Removing the 'text' abstractmethod and property as they don't fit the TTS interface.
# Base directory = project root directory (go up from tts.py location)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Piper folder is at the root
PIPER_DIR = os.path.join(BASE_DIR, "piper")

# Detect executable name (Windows uses .exe, Linux/Mac does not)
if platform.system() == "Windows":
    PIPER_PATH = os.path.join(PIPER_DIR, "piper.exe")
else:
    PIPER_PATH = os.path.join(PIPER_DIR, "piper")

MODEL_PATH = os.path.join(PIPER_DIR, "en_US-amy-low.onnx")

class PIPER_TTS(TTS):
    def __init__(self):
        self._text = ""
    
    @property 
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
    
    def speak(self) -> None:
        try:
            # Debug: Print paths to verify they're correct
            print(f"[TTS Debug] PIPER_PATH: {PIPER_PATH}")
            print(f"[TTS Debug] MODEL_PATH: {MODEL_PATH}")
            print(f"[TTS Debug] Piper exists: {os.path.exists(PIPER_PATH)}")
            print(f"[TTS Debug] Model exists: {os.path.exists(MODEL_PATH)}")
            print(f"[TTS Debug] Text to speak: '{self.text}'")
            
            if not os.path.exists(PIPER_PATH):
                print("[TTS Error] Piper executable not found!")
                print("Fallback (text only):", self.text)
                return
                
            if not os.path.exists(MODEL_PATH):
                print("[TTS Error] Model file not found!")
                print("Fallback (text only):", self.text)
                return

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                wav_path = tmp.name
            # Run Piper
            result = subprocess.run(
                [PIPER_PATH, "--model", MODEL_PATH, "--output_file", wav_path],
                input=self.text,
                text=True,
                capture_output=True
            )

            if result.returncode != 0:
                stderr_text = result.stderr if isinstance(result.stderr, str) else (result.stderr.decode() if result.stderr else "No error details")
                print("[TTS Error] Piper failed:", stderr_text)
                print("Fallback (text only):", self.text)
                return

            # Play audio (Windows only)
            if platform.system() == "Windows":
                winsound.PlaySound(wav_path, winsound.SND_FILENAME)
            else:
                # Linux/Mac fallback: use 'aplay' or 'afplay'
                try:
                    player = "afplay" if platform.system() == "Darwin" else "aplay"
                    subprocess.run([player, wav_path])
                except Exception:
                    print("[Audio Error] Could not play audio. Saved at:", wav_path)
            os.remove(wav_path)
        except Exception as e:
            print("[TTS Error]", e)
            print("Fallback (text only):", self.text)

