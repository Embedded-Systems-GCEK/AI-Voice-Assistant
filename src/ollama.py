import subprocess
from assistant import Assistant 
def ask_ollama(prompt):
    try:
        result = subprocess.run(
            [
                r"ollama run gemma3:1b"
            ],
            input=prompt,
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            print("⚠️ Ollama Error:", result.stderr)
            return "Sorry, I couldn't get a response."
        # Return first 2–3 lines for more complete answers
        lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return ' '.join(lines[:3])  # Join up to 3 lines
    except Exception as e:
        return f"Error communicating with TinyLlama: {e}"

if __name__ == "__main__":
    # Example usage
    assistant = Assistant("CYRUS")
    prompt = "What is the capital of France?"
    response = ask_ollama(prompt)
    print("Ollama response:", response)
    # You can then pass this response to the speak function if needed
    assistant.speak(response)