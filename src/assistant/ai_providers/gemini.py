import google.generativeai as genai

"""If you see a key, here report me immediately.
@ github.com/aruncs31s
Must Load Keys from the .env file or environment variables.
"""
GEMINI_API_KEY = "AIzaSyCBfhLBkCf0wbkgTF8IKu3RJ8LD7G83Tws" 

# Custom Imports
try:
    from .ai_providers import AIProvider, AiProviderList, AiProviderStatus
except ImportError:
    from ai_providers import AIProvider, AiProviderList, AiProviderStatus

class Gemini(AIProvider):
    def __init__(self, api_key: str = GEMINI_API_KEY):
        super().__init__()
        if not api_key:
            raise ValueError("Gemini API key is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")


    @property
    def name(self) -> str:
        return AiProviderList.GEMINI.value

    def _call_api(self, message: list[dict[str, str]] | str) -> str:
        """Implementation of the abstract _call_api method for Gemini"""
        try:
            # Prepare message for Gemini API
            if isinstance(message, str):
                # Single message
                prompt = message
            else:
                # Full conversation history - format for Gemini
                # Convert message format to Gemini's expected format
                gemini_history = []
                
                # Add system prompt first
                system_prompt = {
                    "role": "user",
                    "parts": [
                        "Instruction: You are a helpful AI assistant. "
                        "Always reply briefly, clearly, and to the point (max 2-3 sentences)."
                    ]
                }
                gemini_history.append(system_prompt)
                
                # Convert conversation history
                for msg in message:
                    role = "user" if msg['role'] == 'user' else "model"
                    gemini_history.append({
                        "role": role,
                        "parts": [msg['content']]
                    })
                
                # For conversation history, we'll use the last user message as prompt
                # and send the full history to maintain context
                if gemini_history:
                    response = self.model.generate_content(gemini_history)
                else:
                    response = self.model.generate_content(message[-1]['content'])
                
                assistant_response = getattr(response, "text", "Sorry, I couldn't generate a response.")
                
                if isinstance(message, list):
                    self.add_message("assistant", assistant_response)
                
                return assistant_response.strip()

            # For single string message
            response = self.model.generate_content(prompt)
            assistant_response = getattr(response, "text", "Sorry, I couldn't generate a response.")
            
            return assistant_response.strip()

        except Exception as e:
            self.status = AiProviderStatus.ERROR
            return f"Error communicating with Gemini API: {e}"

    def ask_gemini_api(self, message: list[dict[str, str]] | str) -> str:
        """Legacy method - now delegates to _call_api"""
        return self._call_api(message)

    def ask(self, prompt: str) -> str:
        """Use the generic ask implementation from base class"""
        super().ask(prompt)
        return self._generic_ask(prompt)

if __name__ == "__main__":
    print(f"🤖 Testing {str(Gemini.name).capitalize()} with Memory/Context")
    print("=" * 50)
    # Note: You need to set GEMINI_API_KEY to test this
    if not GEMINI_API_KEY:
        print("⚠️ Please set GEMINI_API_KEY to test Gemini provider")
        exit(1) # To exist

    questions = [
        "Hello! My name is Arun CS",
        "What's my name?",
        "Tell me a short joke"
    ]

    try:
        gemini = Gemini()

        for i, q in enumerate(questions, 1):
            print(f"\n🐸 Arun > {q}")
            answer = gemini.ask(q)
            print(f"🤖 Gemini > {answer}")
            print(f"⏳ Response Time {i}: {gemini.response_time:.2f} seconds")

        print("\n" + "=" * 50)
        print("📚 FULL CONVERSATION HISTORY:")
        gemini.show_conversation_history()

        print("\n📊 CONVERSATION STATISTICS:")
        stats = gemini.get_conversation_stats()
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

        print("\n🧹 Clearing conversation history...")
        print()
        for obj in gemini.QandAs:
            print(obj.to_dict())
        
        gemini.clear_messages()
        gemini.show_conversation_history()

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
