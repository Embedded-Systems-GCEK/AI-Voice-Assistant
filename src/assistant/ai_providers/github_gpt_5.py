import dotenv
from pathlib import Path
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Custom Import
try:
    from .ai_providers import AIProvider, AiProviderList, AiProviderStatus
except ImportError:
    from ai_providers import AIProvider, AiProviderList, AiProviderStatus

from dotenv import load_dotenv
load_dotenv()

token = os.getenv('GITHUB_GPT_5_TOKEN', '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')

class GPT_5(AIProvider):
    def __init__(self, api_token: str = None):
        super().__init__()
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-5"
        
        # Use provided token or environment variable
        self.token = api_token or token
        if not self.token:
            raise ValueError("GITHUB_GPT_5_TOKEN environment variable not set or api_token not provided")
        
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
        )
        
        # Use base class defaults
        # self.temperature = 0.3
        # self.max_tokens = 150

    @property
    def name(self) -> str:
        return AiProviderList.GITHUB_GPT_5.value

    def _call_api(self, message: list[dict[str, str]] | str) -> str:
        """Implementation of the abstract _call_api method for GitHub GPT-5"""
        try:
            # Prepare message for GitHub GPT-5 API
            if isinstance(message, str):
                # Single message
                messages = [UserMessage(message)]
            else:
                # Full conversation history - convert to GitHub AI format
                messages = []
                
                # Add system message for context
                messages.append(SystemMessage("You are a helpful AI assistant. Always reply briefly, clearly, and to the point."))
                
                # Convert conversation history
                for msg in message:
                    if msg['role'] == 'user':
                        messages.append(UserMessage(msg['content']))
                    elif msg['role'] == 'assistant':
                        # Note: GitHub AI format might not support assistant messages in history
                        # For now, we'll focus on the latest user message
                        pass
                
                # If we have conversation history, use the last user message
                if not any(isinstance(msg, UserMessage) for msg in messages[1:]):  # Skip system message
                    # No user messages found, use the last message content
                    last_msg = message[-1] if message else {"content": "Hello"}
                    if last_msg.get('role') == 'user':
                        messages.append(UserMessage(last_msg['content']))

            response = self.client.complete(
                messages=messages,
                model=self.model
            )
            
            assistant_response = response.choices[0].message.content
            
            if isinstance(message, list):
                self.add_message("assistant", assistant_response)
            
            return assistant_response

        except Exception as e:
            self.status = AiProviderStatus.ERROR
            return f"Error communicating with GitHub GPT-5 API: {e}"

    def get_answer(self, message):
        """Legacy method - now delegates to _call_api"""
        return self._call_api(message)

    def ask(self, prompt: str) -> str:
        """Use the generic ask implementation from base class"""
        super().ask(prompt)
        return self._generic_ask(prompt)

if __name__ == "__main__":
    print("🤖 Testing GitHub GPT-5 with Memory/Context")
    print("=" * 50)

    # Note: You need to set GITHUB_GPT_5_TOKEN to test this
    if not token:
        print("⚠️ Please set GITHUB_GPT_5_TOKEN environment variable to test GitHub GPT-5 provider")
        exit(1)

    questions = [
        "Hello! My name is Arun CS",
        "What's my name?",
        "Tell me a short programming joke"
    ]

    try:
        gpt5 = GPT_5()

        for i, q in enumerate(questions, 1):
            print(f"\n🐸 Arun > {q}")
            answer = gpt5.ask(q)
            print(f"🤖 GPT-5 > {answer}")
            print(f"⏳ Response Time {i}: {gpt5.get_response_time():.2f} seconds")

        print("\n" + "=" * 50)
        print("📚 FULL CONVERSATION HISTORY:")
        gpt5.show_conversation_history()

        print("\n📊 CONVERSATION STATISTICS:")
        stats = gpt5.get_conversation_stats()
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

        print("\n🧹 Clearing conversation history...")
        print()
        for obj in gpt5.QandAs:
            print(obj.to_dict())
        
        gpt5.clear_messages()
        gpt5.show_conversation_history()

    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except Exception as e:
        print(f"❌ Error testing GitHub GPT-5: {e}")



