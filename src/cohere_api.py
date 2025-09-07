import cohere

COHERE_API_KEY = "32kO4SNZBl4ofFP2NxSBnmQ8Mm8izj7tcNmJsgh6"
co = cohere.Client(COHERE_API_KEY)

def ask_cohere(query):
    try:
        response = co.chat(message=query, temperature=0.3, max_tokens=50)
        return response.text.strip()
    except Exception as e:
        return f"Cohere API error: {e}"
