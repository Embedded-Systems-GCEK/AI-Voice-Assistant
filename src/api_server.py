#!/usr/bin/env python3
"""
Unified API Server for AI Voice Assistant
Runs the assistant and exposes API endpoints for Flutter integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime
import uuid
from flasgger import Swagger
from enum import Enum


# Custom Imports
from assistant.assistant import ConversationalAssistant
# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Global variables for assistant state
assistant_instance = None
conversation_history = []
current_question = ""
current_answer = ""
question_count = 0

class AsistantStatusErr(Enum):
    FILE = "path not found"
    NET = "network error"
    AUTH = "authentication error"
    ERR = "general error"
    NONE = "no error"
class AssistantStatus(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    READY = "ready"
    ERROR = AsistantStatusErr

assistant_status = AssistantStatus


# Flask app setup
app = Flask(__name__)
swagger = Swagger(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

session_id = str(uuid.uuid4())

class APIServer:
    def __init__(self,assistant: ConversationalAssistant ):
        self.assistant = assistant
        self.assistant_thread = None
        self.running = False
        
    def initialize_assistant(self):
        """Initialize the assistant instance"""
        global assistant_instance, assistant_status
        
        if not check_assistant_modules():
            print("[WARN] Assistant not available")
            return False
            
        try:
            print("[INFO] Initializing AI Assistant...")
            self.status = Status()
            tts = PIPER_TTS()
            ollama = Ollama()
            files = Files()
            
            assistant_instance = ConversationalAssistant(
                name="API Assistant",
                voice_config=None,
                status=self.status,
                tts=tts,
                ollama=ollama,
                files=files
            )
            
            assistant_status = "ready"
            print("[SUCCESS] Assistant initialized successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize assistant: {e}")
            assistant_status = "error"
            return False
    
    def start_assistant_background(self):
        """Start assistant in background thread"""
        if self.initialize_assistant():
            print("[INFO] Assistant running in background, ready for API calls")
            self.running = True
        else:
            print("[ERROR] Failed to start assistant")

# Initialize server
server = APIServer()

# API Endpoints

@app.route('/')
def index():
    return jsonify({
        "message": "AI Voice Assistant API Server",
        "status": "running",
        "assistant_available": ASSISTANT_AVAILABLE,
        "assistant_status": assistant_status,
        "endpoints": [
            "/api/status",
            "/api/ask",
            "/api/conversation",
            "/api/stats",
            "/api/example-questions",
            "/api/reset"
        ]
    })

@app.route('/api/status', methods=['GET'])
def get_assistant_status():
    """Get current assistant status and conversation info"""
    global assistant_instance, current_question, current_answer, question_count, assistant_status
    
    return jsonify({
        "status": "success",
        "data": {
            "assistant_status": assistant_status,
            "assistant_available": ASSISTANT_AVAILABLE,
            "current_question": current_question,
            "current_answer": current_answer,
            "question_count": question_count,
            "session_id": session_id,
            "conversation_length": len(conversation_history),
            "timestamp": datetime.now().isoformat()
        }
    })

@app.route('/api/ask', methods=['POST'])
def ask_assistant():
    """Ask a question to the assistant"""
    global assistant_instance, current_question, current_answer, question_count, assistant_status, conversation_history
    
    try:
        if not assistant_instance:
            return jsonify({
                "status": "error",
                "message": "Assistant not initialized"
            }), 503
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                "status": "error",
                "message": "Question is required"
                
            }), 400
        
        question = data['question']
        user_id = data.get('user_id', 'anonymous')
        
        # Update status
        current_question = question
        assistant_status = "processing"
        question_count += 1
        
        print(f"[INFO] Processing question #{question_count}: {question}")
        
        # Process the question
        try:
            # Use the assistant to process the command/question
            assistant_instance.process_command(question)
            
            # For now, we'll simulate getting a response
            # In a real implementation, you'd capture the assistant's response
            response = f"Processed: {question}"
            
            current_answer = response
            assistant_status = "ready"
            
            # Add to conversation history
            conversation_entry = {
                "id": len(conversation_history) + 1,
                "question": question,
                "answer": response,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "session_id": session_id
            }
            conversation_history.append(conversation_entry)
            
            return jsonify({
                "status": "success",
                "data": {
                    "question": question,
                    "answer": response,
                    "question_number": question_count,
                    "timestamp": datetime.now().isoformat(),
                    "session_id": session_id
                }
            })
            
        except Exception as e:
            assistant_status = "error"
            error_msg = f"Error processing question: {str(e)}"
            print(f"[ERROR] {error_msg}")
            
            return jsonify({
                "status": "error",
                "message": error_msg
            }), 500
            
    except Exception as e:
        assistant_status = "error"
        return jsonify({
            "status": "error",
            "message": f"Request processing error: {str(e)}"
        }), 500

@app.route('/api/conversation', methods=['GET'])
def get_conversation():
    """Get conversation history"""
    global conversation_history
    
    user_id = request.args.get('user_id')
    limit = request.args.get('limit', 50, type=int)
    
    # Filter by user_id if provided
    filtered_history = conversation_history
    if user_id:
        filtered_history = [entry for entry in conversation_history if entry['user_id'] == user_id]
    
    # Limit results
    filtered_history = filtered_history[-limit:]
    
    return jsonify({
        "status": "success",
        "data": {
            "conversation": filtered_history,
            "total_count": len(filtered_history),
            "session_id": session_id
        }
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get conversation statistics"""
    global conversation_history, question_count
    
    return jsonify({
        "status": "success",
        "data": {
            "total_questions": question_count,
            "conversation_entries": len(conversation_history),
            "session_id": session_id,
            "assistant_status": assistant_status,
            "uptime": datetime.now().isoformat()
        }
    })

@app.route('/api/example-questions', methods=['GET'])
def get_example_questions():
    """Get example questions for the Flutter app"""
    
    example_questions = [
        {
            "id": 1,
            "category": "General",
            "question": "What time is it?",
            "description": "Ask for the current time"
        },
        {
            "id": 2,
            "category": "General",
            "question": "What's the date today?",
            "description": "Ask for today's date"
        },
        {
            "id": 3,
            "category": "General",
            "question": "What day is it?",
            "description": "Ask for the current day of the week"
        },
        {
            "id": 4,
            "category": "Personal",
            "question": "How are you?",
            "description": "General greeting and wellbeing check"
        },
        {
            "id": 5,
            "category": "Personal",
            "question": "What's your name?",
            "description": "Ask the assistant's name"
        },
        {
            "id": 6,
            "category": "Knowledge",
            "question": "Tell me about artificial intelligence",
            "description": "Ask about AI concepts"
        },
        {
            "id": 7,
            "category": "Knowledge",
            "question": "What is machine learning?",
            "description": "Ask about ML concepts"
        },
        {
            "id": 8,
            "category": "Technical",
            "question": "How do you work?",
            "description": "Ask about the assistant's functionality"
        },
        {
            "id": 9,
            "category": "Fun",
            "question": "Tell me a joke",
            "description": "Ask for entertainment"
        },
        {
            "id": 10,
            "category": "Fun",
            "question": "What's your favorite color?",
            "description": "Personal preference question"
        }
    ]
    
    category_filter = request.args.get('category')
    if category_filter:
        example_questions = [q for q in example_questions if q['category'].lower() == category_filter.lower()]
    
    return jsonify({
        "status": "success",
        "data": {
            "questions": example_questions,
            "categories": ["General", "Personal", "Knowledge", "Technical", "Fun"]
        }
    })

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset the conversation and assistant state"""
    global conversation_history, current_question, current_answer, question_count, assistant_status, session_id, assistant_instance
    
    try:
        # Reset conversation state
        conversation_history = []
        current_question = ""
        current_answer = ""
        question_count = 0
        session_id = str(uuid.uuid4())
        assistant_status = "ready"
        
        # Reset assistant if available
        if assistant_instance:
            try:
                assistant_instance.reset_conversation()
            except Exception as e:
                print(f"Warning: Could not reset assistant state: {e}")
        
        return jsonify({
            "status": "success",
            "message": "Conversation reset successfully",
            "data": {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Reset failed: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "assistant_available": ASSISTANT_AVAILABLE,
        "assistant_status": assistant_status
    })
# @app.route('/docs', methods=['GET'])
# def docs():


def start_server(port: int, debug: bool = False, threaded: bool = True , host: str = '0.0.0.0'):
    """Start the API server"""
    print("[STARTUP] Starting AI Voice Assistant API Server...")
    print(f"[STARTUP] Server will be available at: {host}:{port}")
    print("[STARTUP] API Documentation:")
    print("   GET  /                    - Server info")
    print("   GET  /api/status          - Assistant status")
    print("   POST /api/ask             - Ask question")
    print("   GET  /api/conversation    - Get conversation history")
    print("   GET  /api/stats           - Get statistics")
    print("   GET  /api/example-questions - Get example questions")
    print("   POST /api/reset           - Reset conversation")
    print("   GET  /health              - Health check")
    print()
    
    # Initialize assistant in background
    server.start_assistant_background()
    
    # Start Flask server
    app.run(host=host, port=port, debug=debug, threaded=threaded)


if __name__ == '__main__':
    start_server(host='0.0.0.0', port=5001, debug=False, threaded=True)
