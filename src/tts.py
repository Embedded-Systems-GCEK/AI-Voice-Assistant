import subprocess
import tempfile
import os

def speak(text):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            wav_path = tmp.name

        subprocess.run([
            "/home/aruncs/piper/piper",
            "--model", "/home/aruncs/piper/en_US-amy-low.onnx",
            "--output_file", wav_path
        ], input=text, text=True, check=True)

        subprocess.run(["aplay", wav_path], check=True)
        os.remove(wav_path)
    except Exception as e:
        print("[TTS Error]", e)
