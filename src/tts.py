import subprocess
import tempfile
import os
import winsound

PIPER_PATH = r"E:\voice-assistant-main\piper\piper.exe"
MODEL_PATH = r"E:\voice-assistant-main\piper\en_US-amy-low.onnx"

def speak(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            wav_path = tmp.name

        # Feed text to Piper via stdin
        result = subprocess.run(
            [PIPER_PATH, "--model", MODEL_PATH, "--output_file", wav_path],
            input=text,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            print("[TTS Error] Piper failed:", result.stderr.decode(errors="ignore"))
            print("Fallback (text only):", text)
            return

        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
        os.remove(wav_path)

    except Exception as e:
        print("[TTS Error]", e)
        print("Fallback (text only):", text)
