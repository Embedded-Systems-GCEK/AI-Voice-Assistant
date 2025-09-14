from ...assistant.ai_providers.ollama import Ollama



if __name__ == "__main__":
    questions = [
        "Who are you?",
        "What is linux?",
        "Can AI really think?"
    ]
    
    ollama  = Ollama()
    for q in questions:
        print(f"Q: {q}")
        answer = ollama.ask(q)
        print(f"A: {answer}\n")
        print(f"Status: {ollama.status}, Answer: {ollama.answer}\n")