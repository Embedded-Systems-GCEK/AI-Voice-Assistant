import requests
import pygame  # For music control
import time
import re

file = "piper_output.wav"
ip = "192.168.31.17"
port = "10200"
end_point = "/api/text-to-speech"
voice = "en_US-lessac-medium"  # Default voice
piper_url = f"http://{ip}:{port}{end_point}?voice={voice}"

def save_to_file(response):
    with open(file, "wb") as f:
        f.write(response.content)
        # Play the audio
def play_audio(file="piper_output.wav"):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()


def get_text(chunk_text):
    try:
        return requests.post(
            piper_url,
            data=chunk_text.encode('utf-8'),
            headers={'Content-Type': 'text/plain'}
        )
    except Exception as e:
        print("Piper request failed:", e)


if __name__ == "__main__":
    # TTS Test example
    text = "Hello, this is a test of the text  to speech system."
    speak(text)