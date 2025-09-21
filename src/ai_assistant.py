"""
AI Assistant module that integrates various components such as speech recognition,
"""

# Import all AI Providers 

from assistant.ai_providers.ai_providers import AIProvider
from assistant.ai_providers.ollama import Ollama
from assistant.ai_providers.github_gpt_5 import GPT_5
from assistant.ai_providers.cohere_api import CohereAPI
from assistant.ai_providers.gemini import Gemini
from assistant.ai_providers.llama import Llama

# Files 
from assistant.files.files import Files
# Answer Helper


from assistant.assistant import ConversationalAssistant
class AIProviderStatus:
    IDLE = "idle"
    BUSY = "busy"
    """Latter Used to indicate an error state"""
    ERROR = "error"



class AIAssistant(ConversationalAssistant):
    def __init__(
        self,
        ai_provider: AIProvider = Ollama(),
        name: str = "AI Assistant"
    ):
        super().__init__(
            ai_provider=ai_provider,
            name=name
        )
    def change_ai_provider(self, new_provider: AIProvider) -> None:
        self.ai_provider = new_provider
        print(f"🤖 AI Provider changed to {new_provider.name}")
    def ask(self,prompt: str):
        self.response = self.ai_provider.ask_with_timeout(prompt)
        self.answer(self.response)
        return self.response
# ai_providers = {
#     "ollama": {
#         "instance": Ollama(),
#         "status": AIProviderStatus.IDLE
#     },
#     "github_gpt_5": {
#         "instance": GPT_5(),
#         "status": AIProviderStatus.IDLE
#     },
# }

# def check_ai_providers():
#     for name, provider in ai_provders.items():
#         try:
#             print(f"Checking AI Provider: {name}")
#             response = provider.ask("What is the capital of France?")
#             print(f"Response from {name}: {response}")
#         except Exception as e:
#             print(f"Error with {name}: {e}")
      
def test_ai_assistant():
    assistant = AIAssistant()
    query = "What is you name?"
    response = assistant.ask(query)
    print(f"🤖 Response from {assistant.ai_provider.name} : {response} \n",
          f"⏳ Response Time: {assistant.ai_provider.response_time} seconds\n")
    # print()
    # assistant.ai_provider = GPT_5()
    # response = assistant.ask(query)
    # print(f"🤖 Response from {assistant.ai_provider.name}: {response} \n",
    #       f"⏳ Response Time: {assistant.ai_provider.response_time} seconds")
    # print()
    
    # assistant.ai_provider = CohereAPI()
    # response = assistant.ask(query)
    # print(f"🤖 Response from {assistant.ai_provider.name}: {response} \n",
    #       f"⏳ Response Time: {assistant.ai_provider.response_time} seconds")
    # print()
    
    # assistant.ai_provider = Gemini()
    # response = assistant.ask(query)
    # print(f"🤖 Response from {assistant.ai_provider.name}: {response} \n",
    #       f"⏳ Response Time: {assistant.ai_provider.response_time} seconds")
    # print()

if __name__ == "__main__":
    test_ai_assistant()
