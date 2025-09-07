
import subprocess
import tempfile
import os
import platform
import winsound

# Base directory = where this file lives (src/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Piper folder is one level up (../piper/)
PIPER_DIR = os.path.join(BASE_DIR, "..", "piper")

# Detect executable name (Windows uses .exe, Linux/Mac does not)
if platform.system() == "Windows":
    PIPER_PATH = os.path.join(PIPER_DIR, "piper.exe")
else:
    PIPER_PATH = os.path.join(PIPER_DIR, "piper")

MODEL_PATH = os.path.join(PIPER_DIR, "en_US-amy-low.onnx")

def speak(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            wav_path = tmp.name

        # Run Piper
        result = subprocess.run(
            [PIPER_PATH, "--model", MODEL_PATH, "--output_file", wav_path],
            input=text,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            print("[TTS Error] Piper failed:", result.stderr)
            print("Fallback (text only):", text)
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
        print("Fallback (text only):", text)

