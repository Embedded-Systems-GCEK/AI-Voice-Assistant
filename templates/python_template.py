"""
AI Voice Assistant - Python API Integration Template
Complete implementation example for Python applications
"""

import requests
import asyncio
import aiohttp
import time
import json
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
import threading


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class AssistantStatus:
    """Assistant status information"""
    assistant_status: str
    assistant_available: bool
    current_question: str
    current_answer: str
    question_count: int
    session_id: str
    conversation_length: int
    timestamp: datetime
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AssistantStatus':
        return cls(
            assistant_status=data.get('assistant_status', 'unknown'),
            assistant_available=data.get('assistant_available', False),
            current_question=data.get('current_question', ''),
            current_answer=data.get('current_answer', ''),
            question_count=data.get('question_count', 0),
            session_id=data.get('session_id', ''),
            conversation_length=data.get('conversation_length', 0),
            timestamp=datetime.fromisoformat(data['timestamp'])
        )

@dataclass
class QuestionResponse:
    """Response from asking a question"""
    question: str
    answer: str
    question_number: int
    timestamp: datetime
    session_id: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'QuestionResponse':
        return cls(
            question=data.get('question', ''),
            answer=data.get('answer', ''),
            question_number=data.get('question_number', 0),
            timestamp=datetime.fromisoformat(data['timestamp']),
            session_id=data.get('session_id', '')
        )

@dataclass
class ConversationEntry:
    """Single conversation entry"""
    id: int
    question: str
    answer: str
    timestamp: datetime
    user_id: str
    session_id: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationEntry':
        return cls(
            id=data.get('id', 0),
            question=data.get('question', ''),
            answer=data.get('answer', ''),
            timestamp=datetime.fromisoformat(data['timestamp']),
            user_id=data.get('user_id', ''),
            session_id=data.get('session_id', '')
        )

@dataclass
class AssistantStats:
    """Assistant statistics"""
    total_questions: int
    conversation_entries: int
    session_id: str
    assistant_status: str
    uptime: datetime
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AssistantStats':
        return cls(
            total_questions=data.get('total_questions', 0),
            conversation_entries=data.get('conversation_entries', 0),
            session_id=data.get('session_id', ''),
            assistant_status=data.get('assistant_status', 'unknown'),
            uptime=datetime.fromisoformat(data['uptime'])
        )

@dataclass
class ExampleQuestion:
    """Example question from the API"""
    id: int
    category: str
    question: str
    description: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExampleQuestion':
        return cls(
            id=data.get('id', 0),
            category=data.get('category', ''),
            question=data.get('question', ''),
            description=data.get('description', '')
        )


# =============================================================================
# SYNCHRONOUS API CLIENT
# =============================================================================

class AssistantApiClient:
    """Synchronous API client for AI Voice Assistant"""
    
    def __init__(self, base_url: str = "http://localhost:5001", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('status') == 'error':
                raise Exception(result.get('message', 'API Error'))
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
    
    def get_status(self) -> AssistantStatus:
        """GET /api/status - Get current assistant status"""
        response = self._make_request('GET', '/api/status')
        return AssistantStatus.from_dict(response['data'])
    
    def ask_question(self, question: str, user_id: Optional[str] = None) -> QuestionResponse:
        """POST /api/ask - Ask a question"""
        data = {'question': question}
        if user_id:
            data['user_id'] = user_id
        
        response = self._make_request('POST', '/api/ask', data=data)
        return QuestionResponse.from_dict(response['data'])
    
    def get_conversation(self, user_id: Optional[str] = None, limit: Optional[int] = None) -> List[ConversationEntry]:
        """GET /api/conversation - Get conversation history"""
        params = {}
        if user_id:
            params['user_id'] = user_id
        if limit:
            params['limit'] = str(limit)
        
        response = self._make_request('GET', '/api/conversation', params=params)
        conversation_data = response['data']['conversation']
        
        return [ConversationEntry.from_dict(item) for item in conversation_data]
    
    def get_stats(self) -> AssistantStats:
        """GET /api/stats - Get statistics"""
        response = self._make_request('GET', '/api/stats')
        return AssistantStats.from_dict(response['data'])
    
    def get_example_questions(self, category: Optional[str] = None) -> List[ExampleQuestion]:
        """GET /api/example-questions - Get example questions"""
        params = {}
        if category:
            params['category'] = category
        
        response = self._make_request('GET', '/api/example-questions', params=params)
        questions_data = response['data']['questions']
        
        return [ExampleQuestion.from_dict(item) for item in questions_data]
    
    def reset_conversation(self) -> Dict:
        """POST /api/reset - Reset conversation"""
        response = self._make_request('POST', '/api/reset')
        return response['data']
    
    def check_health(self) -> bool:
        """GET /health - Health check"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_status_polling(self, callback: Callable[[Optional[Exception], Optional[AssistantStatus]], None], 
                           interval: float = 2.0) -> Callable[[], None]:
        """Start polling for status updates"""
        stop_event = threading.Event()
        
        def poll():
            while not stop_event.is_set():
                try:
                    status = self.get_status()
                    callback(None, status)
                except Exception as e:
                    callback(e, None)
                
                stop_event.wait(interval)
        
        thread = threading.Thread(target=poll, daemon=True)
        thread.start()
        
        # Return stop function
        return stop_event.set


# =============================================================================
# ASYNCHRONOUS API CLIENT
# =============================================================================

class AsyncAssistantApiClient:
    """Asynchronous API client for AI Voice Assistant"""
    
    def __init__(self, base_url: str = "http://localhost:5001", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                           params: Optional[Dict] = None) -> Dict:
        """Make async HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        async with aiohttp.ClientSession(timeout=self.timeout, headers=self.headers) as session:
            try:
                async with session.request(method, url, json=data, params=params) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    if result.get('status') == 'error':
                        raise Exception(result.get('message', 'API Error'))
                    
                    return result
                    
            except aiohttp.ClientError as e:
                raise Exception(f"Request failed: {str(e)}")
            except json.JSONDecodeError as e:
                raise Exception(f"Invalid JSON response: {str(e)}")
    
    async def get_status(self) -> AssistantStatus:
        """GET /api/status - Get current assistant status"""
        response = await self._make_request('GET', '/api/status')
        return AssistantStatus.from_dict(response['data'])
    
    async def ask_question(self, question: str, user_id: Optional[str] = None) -> QuestionResponse:
        """POST /api/ask - Ask a question"""
        data = {'question': question}
        if user_id:
            data['user_id'] = user_id
        
        response = await self._make_request('POST', '/api/ask', data=data)
        return QuestionResponse.from_dict(response['data'])
    
    async def get_conversation(self, user_id: Optional[str] = None, limit: Optional[int] = None) -> List[ConversationEntry]:
        """GET /api/conversation - Get conversation history"""
        params = {}
        if user_id:
            params['user_id'] = user_id
        if limit:
            params['limit'] = str(limit)
        
        response = await self._make_request('GET', '/api/conversation', params=params)
        conversation_data = response['data']['conversation']
        
        return [ConversationEntry.from_dict(item) for item in conversation_data]
    
    async def get_stats(self) -> AssistantStats:
        """GET /api/stats - Get statistics"""
        response = await self._make_request('GET', '/api/stats')
        return AssistantStats.from_dict(response['data'])
    
    async def get_example_questions(self, category: Optional[str] = None) -> List[ExampleQuestion]:
        """GET /api/example-questions - Get example questions"""
        params = {}
        if category:
            params['category'] = category
        
        response = await self._make_request('GET', '/api/example-questions', params=params)
        questions_data = response['data']['questions']
        
        return [ExampleQuestion.from_dict(item) for item in questions_data]
    
    async def reset_conversation(self) -> Dict:
        """POST /api/reset - Reset conversation"""
        response = await self._make_request('POST', '/api/reset')
        return response['data']
    
    async def check_health(self) -> bool:
        """GET /health - Health check"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(f"{self.base_url}/health") as response:
                    return response.status == 200
        except:
            return False


# =============================================================================
# FLASK INTEGRATION EXAMPLE
# =============================================================================

from flask import Flask, request, jsonify, render_template_string

def create_flask_app(assistant_api_url: str = "http://localhost:5001"):
    """Create Flask app with assistant integration"""
    app = Flask(__name__)
    client = AssistantApiClient(assistant_api_url)
    
    @app.route('/')
    def index():
        """Main chat interface"""
        return render_template_string(FLASK_TEMPLATE)
    
    @app.route('/api/status')
    def api_status():
        """Proxy to assistant status"""
        try:
            status = client.get_status()
            return jsonify({
                'status': 'success',
                'data': {
                    'assistant_status': status.assistant_status,
                    'current_question': status.current_question,
                    'current_answer': status.current_answer,
                    'question_count': status.question_count,
                    'session_id': status.session_id
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/ask', methods=['POST'])
    def api_ask():
        """Proxy to assistant ask"""
        try:
            data = request.get_json()
            question = data.get('question')
            user_id = data.get('user_id')
            
            if not question:
                return jsonify({'status': 'error', 'message': 'Question is required'}), 400
            
            response = client.ask_question(question, user_id)
            return jsonify({
                'status': 'success',
                'data': {
                    'question': response.question,
                    'answer': response.answer,
                    'question_number': response.question_number,
                    'timestamp': response.timestamp.isoformat()
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/conversation')
    def api_conversation():
        """Proxy to conversation history"""
        try:
            user_id = request.args.get('user_id')
            limit = request.args.get('limit', type=int)
            
            conversation = client.get_conversation(user_id, limit)
            return jsonify({
                'status': 'success',
                'data': {
                    'conversation': [
                        {
                            'id': entry.id,
                            'question': entry.question,
                            'answer': entry.answer,
                            'timestamp': entry.timestamp.isoformat(),
                            'user_id': entry.user_id
                        }
                        for entry in conversation
                    ]
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/api/reset', methods=['POST'])
    def api_reset():
        """Proxy to reset conversation"""
        try:
            result = client.reset_conversation()
            return jsonify({'status': 'success', 'data': result})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    @app.route('/health')
    def health():
        """Health check"""
        assistant_healthy = client.check_health()
        return jsonify({
            'status': 'healthy' if assistant_healthy else 'unhealthy',
            'assistant_available': assistant_healthy
        })
    
    return app


# =============================================================================
# FASTAPI INTEGRATION EXAMPLE
# =============================================================================

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    
    class AskRequest(BaseModel):
        question: str
        user_id: Optional[str] = None
    
    def create_fastapi_app(assistant_api_url: str = "http://localhost:5001"):
        """Create FastAPI app with assistant integration"""
        app = FastAPI(title="AI Assistant Proxy", version="1.0.0")
        client = AsyncAssistantApiClient(assistant_api_url)
        
        @app.get("/status")
        async def get_status():
            """Get assistant status"""
            try:
                status = await client.get_status()
                return {
                    'assistant_status': status.assistant_status,
                    'current_question': status.current_question,
                    'current_answer': status.current_answer,
                    'question_count': status.question_count,
                    'session_id': status.session_id
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/ask")
        async def ask_question(request: AskRequest):
            """Ask a question"""
            try:
                response = await client.ask_question(request.question, request.user_id)
                return {
                    'question': response.question,
                    'answer': response.answer,
                    'question_number': response.question_number,
                    'timestamp': response.timestamp.isoformat()
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/conversation")
        async def get_conversation(user_id: Optional[str] = None, limit: Optional[int] = None):
            """Get conversation history"""
            try:
                conversation = await client.get_conversation(user_id, limit)
                return {
                    'conversation': [
                        {
                            'id': entry.id,
                            'question': entry.question,
                            'answer': entry.answer,
                            'timestamp': entry.timestamp.isoformat(),
                            'user_id': entry.user_id
                        }
                        for entry in conversation
                    ]
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/reset")
        async def reset_conversation():
            """Reset conversation"""
            try:
                result = await client.reset_conversation()
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        return app

except ImportError:
    # FastAPI not available
    def create_fastapi_app(*args, **kwargs):
        raise ImportError("FastAPI not installed. Install with: pip install fastapi uvicorn")


# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

import argparse
import sys

class ChatCLI:
    """Command line chat interface"""
    
    def __init__(self, api_url: str = "http://localhost:5001"):
        self.client = AssistantApiClient(api_url)
        
    def run(self):
        """Run interactive chat"""
        print("AI Voice Assistant - Command Line Interface")
        print("Type 'quit' to exit, 'status' for status, 'reset' to reset conversation")
        print("-" * 60)
        
        # Check health
        if not self.client.check_health():
            print("ERROR: Assistant API is not available!")
            return
        
        # Show initial status
        try:
            status = self.client.get_status()
            print(f"Connected to assistant. Questions asked: {status.question_count}")
        except Exception as e:
            print(f"Warning: Could not get status - {e}")
        
        print("-" * 60)
        
        # Chat loop
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_input.lower() == 'status':
                    self._show_status()
                    continue
                elif user_input.lower() == 'reset':
                    self._reset_conversation()
                    continue
                elif not user_input:
                    continue
                
                # Ask question
                print("Assistant: Processing...")
                response = self.client.ask_question(user_input)
                print(f"Assistant: {response.answer}")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\nGoodbye!")
    
    def _show_status(self):
        """Show current status"""
        try:
            status = self.client.get_status()
            stats = self.client.get_stats()
            
            print("\n--- Assistant Status ---")
            print(f"Status: {status.assistant_status}")
            print(f"Questions asked: {status.question_count}")
            print(f"Session ID: {status.session_id}")
            print(f"Last question: {status.current_question or 'None'}")
            print(f"Last answer: {status.current_answer or 'None'}")
            print(f"Total conversation entries: {stats.conversation_entries}")
            
        except Exception as e:
            print(f"Error getting status: {e}")
    
    def _reset_conversation(self):
        """Reset conversation"""
        try:
            result = self.client.reset_conversation()
            print(f"Conversation reset. New session: {result['session_id']}")
        except Exception as e:
            print(f"Error resetting conversation: {e}")


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def sync_example():
    """Example using synchronous client"""
    print("=== Synchronous API Example ===")
    
    client = AssistantApiClient()
    
    try:
        # Check health
        if not client.check_health():
            print("Assistant API is not available!")
            return
        
        # Get status
        status = client.get_status()
        print(f"Status: {status.assistant_status}")
        print(f"Questions asked: {status.question_count}")
        
        # Ask a question
        print("\nAsking: 'What time is it?'")
        response = client.ask_question("What time is it?")
        print(f"Answer: {response.answer}")
        
        # Get conversation
        conversation = client.get_conversation(limit=5)
        print(f"\nConversation has {len(conversation)} entries")
        
        # Get example questions
        examples = client.get_example_questions()
        print(f"\nExample questions available: {len(examples)}")
        for example in examples[:3]:
            print(f"  - {example.question} ({example.category})")
        
    except Exception as e:
        print(f"Error: {e}")


async def async_example():
    """Example using asynchronous client"""
    print("=== Asynchronous API Example ===")
    
    client = AsyncAssistantApiClient()
    
    try:
        # Check health
        if not await client.check_health():
            print("Assistant API is not available!")
            return
        
        # Get status
        status = await client.get_status()
        print(f"Status: {status.assistant_status}")
        print(f"Questions asked: {status.question_count}")
        
        # Ask multiple questions concurrently
        questions = ["What time is it?", "How are you?", "What's your name?"]
        
        print(f"\nAsking {len(questions)} questions concurrently...")
        tasks = [client.ask_question(q) for q in questions]
        responses = await asyncio.gather(*tasks)
        
        for question, response in zip(questions, responses):
            print(f"Q: {question}")
            print(f"A: {response.answer}")
            print()
        
        # Get updated conversation
        conversation = await client.get_conversation()
        print(f"Conversation now has {len(conversation)} entries")
        
    except Exception as e:
        print(f"Error: {e}")


def flask_example():
    """Example Flask app"""
    app = create_flask_app()
    print("Starting Flask app on http://localhost:5003")
    print("Visit the URL to see the web interface")
    app.run(host='0.0.0.0', port=5003, debug=True)


# =============================================================================
# FLASK TEMPLATE
# =============================================================================

FLASK_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Assistant Chat</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .chat-container { max-width: 800px; margin: 0 auto; }
        .messages { height: 400px; border: 1px solid #ddd; padding: 10px; overflow-y: auto; margin: 20px 0; }
        .message { margin: 10px 0; }
        .user-message { text-align: right; }
        .assistant-message { text-align: left; }
        .message-bubble { display: inline-block; padding: 10px; border-radius: 10px; max-width: 70%; }
        .user-bubble { background-color: #007bff; color: white; }
        .assistant-bubble { background-color: #f1f1f1; }
        .input-area { display: flex; gap: 10px; }
        .input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .input-area button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .status { margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>AI Assistant Chat</h1>
        <div id="status" class="status"></div>
        <div id="messages" class="messages"></div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Ask a question..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
            <button onclick="resetConversation()">Reset</button>
        </div>
    </div>

    <script>
        let conversation = [];
        
        // Load initial data
        loadConversation();
        loadStatus();
        
        // Auto-refresh status
        setInterval(loadStatus, 2000);
        
        async function loadStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                if (data.status === 'success') {
                    document.getElementById('status').innerHTML = 
                        `Status: ${data.data.assistant_status} | Questions: ${data.data.question_count} | Session: ${data.data.session_id}`;
                    document.getElementById('status').className = 'status';
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                document.getElementById('status').innerHTML = `Error: ${error.message}`;
                document.getElementById('status').className = 'status error';
            }
        }
        
        async function loadConversation() {
            try {
                const response = await fetch('/api/conversation');
                const data = await response.json();
                
                if (data.status === 'success') {
                    conversation = data.data.conversation;
                    displayMessages();
                }
            } catch (error) {
                console.error('Failed to load conversation:', error);
            }
        }
        
        function displayMessages() {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML = conversation.map(entry => `
                <div class="message user-message">
                    <div class="message-bubble user-bubble">${entry.question}</div>
                </div>
                <div class="message assistant-message">
                    <div class="message-bubble assistant-bubble">${entry.answer}</div>
                </div>
            `).join('');
            
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            input.value = '';
            input.disabled = true;
            
            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: message })
                });
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    await loadConversation();
                } else {
                    alert(`Error: ${data.message}`);
                }
            } catch (error) {
                alert(`Error: ${error.message}`);
            } finally {
                input.disabled = false;
                input.focus();
            }
        }
        
        async function resetConversation() {
            if (!confirm('Reset conversation?')) return;
            
            try {
                const response = await fetch('/api/reset', { method: 'POST' });
                const data = await response.json();
                
                if (data.status === 'success') {
                    conversation = [];
                    displayMessages();
                    await loadStatus();
                } else {
                    alert(`Error: ${data.message}`);
                }
            } catch (error) {
                alert(`Error: ${error.message}`);
            }
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
"""


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="AI Assistant Python Client")
    parser.add_argument('--url', default='http://localhost:5001', help='Assistant API URL')
    parser.add_argument('--mode', choices=['sync', 'async', 'cli', 'flask'], 
                       default='cli', help='Example mode to run')
    
    args = parser.parse_args()
    
    if args.mode == 'sync':
        sync_example()
    elif args.mode == 'async':
        asyncio.run(async_example())
    elif args.mode == 'cli':
        ChatCLI(args.url).run()
    elif args.mode == 'flask':
        flask_example()


if __name__ == "__main__":
    main()
