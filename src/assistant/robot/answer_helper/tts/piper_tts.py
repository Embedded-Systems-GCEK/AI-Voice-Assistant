import subprocess
import tempfile
import os
import platform
import winsound
import threading

from tts import TTS, TTSState

# Base directory = project root directory (go up from tts.py location)
BASE_DIR =  os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

# Piper folder is at the root
PIPER_DIR = os.path.join(BASE_DIR, "piper")

# Detect executable name (Windows uses .exe, Linux/Mac does not)
if platform.system() == "Windows":
    PIPER_PATH = os.path.join( "..",PIPER_DIR,"piper.exe")
else:
    PIPER_PATH = os.path.join("..",PIPER_DIR,  "piper")

MODEL_PATH = os.path.join(".." ,PIPER_DIR, "en_US-amy-low.onnx")
class PIPER_TTS(TTS):
    def __init__(self):
        super().__init__()
        self._text = ""
        self._thread = None

    def speak(self, text: str) -> None:
        super().speak(text)
        self._thread = threading.Thread(target=self._speak_internal, args=(text,))
        self._thread.start()

    def _speak_internal(self, text: str) -> None:
        try:
            if not os.path.exists(PIPER_PATH) or not os.path.exists(MODEL_PATH):
                self.state = TTSState.ERROR
                print("Missing Piper or model")
                return
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                wav_path = tmp.name
            result = subprocess.run(
                [PIPER_PATH, "--model", MODEL_PATH, "--output_file", wav_path],
                input=text,
                text=True,
                capture_output=True
            )

            if result.returncode != 0:
                self.state = TTSState.ERROR
                print("[TTS Error] Piper failed:", result.stderr)
                return

            self.state = TTSState.SPEAKING
            if platform.system() == "Windows":
                winsound.PlaySound(wav_path, winsound.SND_FILENAME)
            else:
                player = "afplay" if platform.system() == "Darwin" else "aplay"
                subprocess.run([player, wav_path])

            self.state = TTSState.IDLE
            # Spawn a thread just for cleanup
            threading.Thread(target=self.remove_wav_file, args=(wav_path,), daemon=True).start()


        except Exception as e:
            self.state = TTSState.ERROR
            print("[TTS Error]", e)
    def remove_wav_file(self, wav_path: str) -> None:
            """Delete wav file in a background thread"""
            try:
                if os.path.exists(wav_path):
                    os.remove(wav_path)
                    # Debug: print(f"[TTS Cleanup] Removed {wav_path}")
            except Exception as e:
                print(f"[TTS Cleanup Error] Could not delete {wav_path}: {e}")
    def is_done(self) -> bool:
        return self.state == TTSState.IDLE and (self._thread is None or not self._thread.is_alive())
    
    

def test_any_tts():
    tts = PIPER_TTS()
    tts.speak("Hello, this is a test of the Piper Text-to-Speech system.")
    while not tts.is_done():
        pass
    print("Test finished.")

if __name__ == "__main__":
    test_any_tts()
    