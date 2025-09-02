import subprocess

def ask_ollama(prompt):
    try:
        formatted_prompt = f"Answer clearly and briefly: {prompt}"
        result = subprocess.run(
            f"echo {formatted_prompt!r} | ollama run mistral:7b",
            shell=True, capture_output=True, text=True
        )
        if result.returncode != 0:
            print("Ollama error:", result.stderr)
            return "Sorry, I couldn't get a response."
        lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return ' '.join(lines[:3])
    except Exception as e:
        return f"Error communicating with Ollama: {e}"
