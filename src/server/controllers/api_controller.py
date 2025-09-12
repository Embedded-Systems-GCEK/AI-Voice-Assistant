from models.models import User, QuestionResponse
from database.db_helper import DatabaseHelper
from handlers.request_handler import RequestHandler, ResponseHandler
from datetime import datetime
import sys
import os

# Add parent directory to path to import assistant modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from assistant.assistant import ConversationalAssistant
    from assistant.status.status import Status
    from assistant.robot.answer_helper.tts.tts import PIPER_TTS
    from assistant.ai_providers.ollama import Ollama
    from assistant.files.files import Files
    ASSISTANT_AVAILABLE = True
except ImportError:
    ASSISTANT_AVAILABLE = False
    print("Assistant modules not available")

class APIController:
    """Controller for handling API endpoints"""
    
    # Example questions for the Flutter app
    EXAMPLE_QUESTIONS = [
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
            "category": "Knowledge",
            "question": "Tell me about artificial intelligence",
            "description": "Learn about AI concepts"
        }
    ]
    
    # Initialize assistant instance
    assistant_instance = None
    
    @classmethod
    def initialize_assistant(cls):
        """Initialize the assistant instance"""
        if ASSISTANT_AVAILABLE and not cls.assistant_instance:
            try:
                status = Status()
                tts = PIPER_TTS()
                ollama = Ollama()
                files = Files()
                cls.assistant_instance = ConversationalAssistant(
                    name="ARIA", 
                    status=status, 
                    tts=tts, 
                    ollama=ollama, 
                    files=files
                )
                print("Assistant initialized successfully")
            except Exception as e:
                global ASSISTANT_AVAILABLE
                print(f"Failed to initialize assistant: {e}")
                ASSISTANT_AVAILABLE = False
    
    @staticmethod
    def get_example_questions():
        """Get example questions for the Flutter app"""
        try:
            query_params = RequestHandler.get_query_params()
            category = query_params.get('category')
            
            if category:
                filtered_questions = [q for q in APIController.EXAMPLE_QUESTIONS 
                                    if q['category'].lower() == category.lower()]
                return ResponseHandler.success('Example questions retrieved successfully', {
                    'questions': filtered_questions,
                    'total': len(filtered_questions)
                })
            
            return ResponseHandler.success('Example questions retrieved successfully', {
                'questions': APIController.EXAMPLE_QUESTIONS,
                'total': len(APIController.EXAMPLE_QUESTIONS),
                'categories': list(set(q['category'] for q in APIController.EXAMPLE_QUESTIONS))
            })
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @classmethod
    def ask_assistant(cls):
        """Ask a question to the AI assistant"""
        try:
            data = RequestHandler.get_json_data()
            
            # Validate required fields
            is_valid, error_msg = RequestHandler.validate_required_fields(data, ['question'])
            if not is_valid:
                return ResponseHandler.validation_error(error_msg)
            
            question = data['question']
            user_id = data.get('user_id')
            
            # Verify user exists if user_id is provided
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    return ResponseHandler.not_found('User')
            
            start_time = datetime.now()
            
            # Initialize assistant if not already done
            cls.initialize_assistant()
            
            # Get response from assistant
            response_text = ""
            confidence_score = None
            
            if ASSISTANT_AVAILABLE and cls.assistant_instance:
                try:
                    # Use assistant to process the question
                    cls.assistant_instance.question = question
                    cls.assistant_instance.process_command(question)
                    response_text = cls.assistant_instance.response or "I'm not sure how to respond to that."
                    confidence_score = 0.8  # Mock confidence score
                except Exception as e:
                    response_text = f"Sorry, I encountered an error: {str(e)}"
                    confidence_score = 0.1
            else:
                # Fallback responses when assistant is not available
                fallback_responses = {
                    'time': f"The current time is {datetime.now().strftime('%I:%M %p')}",
                    'date': f"Today's date is {datetime.now().strftime('%B %d, %Y')}",
                    'day': f"Today is {datetime.now().strftime('%A')}",
                    'hello': "Hello! How can I help you today?",
                    'how are you': "I'm doing well, thank you for asking!",
                    'name': "I'm ARIA, your AI assistant.",
                    'help': "I can help you with questions about time, date, general information, and more!"
                }
                
                question_lower = question.lower()
                response_text = "I'm not sure how to respond to that."
                
                for key, fallback in fallback_responses.items():
                    if key in question_lower:
                        response_text = fallback
                        confidence_score = 0.9
                        break
                
                if confidence_score is None:
                    confidence_score = 0.3
            
            end_time = datetime.now()
            response_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # Save to database if user_id is provided
            if user_id:
                question_response = QuestionResponse(
                    user_id=user_id,
                    question=question,
                    response=response_text,
                    confidence_score=confidence_score,
                    response_time_ms=response_time_ms
                )
                DatabaseHelper.save(question_response)
            
            return ResponseHandler.success('Question processed successfully', {
                'question': question,
                'response': response_text,
                'confidence_score': confidence_score,
                'response_time_ms': response_time_ms,
                'timestamp': datetime.now().isoformat(),
                'user_id': user_id
            })
            
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def get_user_conversation(user_id: str):
        """Get conversation history for a specific user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return ResponseHandler.not_found('User')
            
            query_params = RequestHandler.get_query_params()
            limit = int(query_params.get('limit', 50))
            offset = int(query_params.get('offset', 0))
            
            conversations = QuestionResponse.query.filter_by(user_id=user_id)\
                .order_by(QuestionResponse.timestamp.desc())\
                .limit(limit)\
                .offset(offset)\
                .all()
            
            return ResponseHandler.success('Conversation history retrieved successfully', {
                'user': user.to_dict(),
                'conversations': [conv.to_dict() for conv in conversations],
                'total': QuestionResponse.query.filter_by(user_id=user_id).count()
            })
            
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @classmethod
    def get_assistant_status(cls):
        """Get current assistant status"""
        try:
            status_info = {
                'available': ASSISTANT_AVAILABLE,
                'initialized': cls.assistant_instance is not None,
                'name': cls.assistant_instance.name if cls.assistant_instance else None,
                'is_connected': cls.assistant_instance.is_connected() if cls.assistant_instance else False
            }
            
            return ResponseHandler.success('Assistant status retrieved successfully', status_info)
            
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @classmethod
    def reset_assistant(cls):
        """Reset assistant conversation state"""
        try:
            if not ASSISTANT_AVAILABLE or not cls.assistant_instance:
                return ResponseHandler.error('Assistant not available', 503)
            
            # Reset assistant state if method exists
            if hasattr(cls.assistant_instance, 'reset_conversation'):
                cls.assistant_instance.reset_conversation()
            
            return ResponseHandler.success('Assistant conversation reset successfully', {
                'status': 'reset'
            })
            
        except Exception as e:
            return ResponseHandler.server_error(str(e))
