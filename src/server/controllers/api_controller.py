from ..models.models import User, QuestionResponse
from ..database.db_helper import DatabaseHelper
from ..handlers.request_handler import RequestHandler, ResponseHandler
from ..dto.request_dto import AskQuestionDTO, ConversationQueryDTO
from ..dto.response_dto import (
    AskQuestionResponseDTO,
    ConversationResponseDTO,
    AssistantStatusDTO,
)
from datetime import datetime
import sys
import os

# Add parent directory to path to import assistant modules
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from ...ai_assistant import get_ai_assistant, initialize_ai_assistant, AISingleton
    ASSISTANT_AVAILABLE = True
except ImportError:
    ASSISTANT_AVAILABLE = False
    print("Assistant modules not available")

class AssistantAPIController:
    """Controller for handling API endpoints"""
    
    # Initialize assistant instance
    assistant_instance = None
    
    @classmethod
    def initialize_assistant(cls):
        """Initialize the singleton assistant instance"""
        global ASSISTANT_AVAILABLE
        if ASSISTANT_AVAILABLE and not AISingleton.is_initialized():
            try:
                # Initialize the singleton AI assistant
                initialize_ai_assistant(name="Minix")
                print("Assistant initialized successfully")
            except Exception as e:
                print(f"Failed to initialize assistant: {e}")
                ASSISTANT_AVAILABLE = False
    
    
    @classmethod
    def ask_assistant(cls):
        """Ask a question to the AI assistant"""
        try:
            data , err = RequestHandler.get_json_data()
            if err:
                return ResponseHandler.validation_error(f"Invalid JSON data: {err}")
            # Use DTO for validation
            try:
                dto = AskQuestionDTO.from_dict(data)
                is_valid, error_msg = dto.validate()
                if not is_valid:
                    return ResponseHandler.validation_error(error_msg)
            except ValueError as e:
                return ResponseHandler.validation_error(str(e))
            
            question = dto.question
            user_id = dto.user_id
            
            # Verify user exists if user_id is provided
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    return ResponseHandler.not_found('User')
            
            start_time = datetime.now()
            
            # Initialize assistant if not already done
            # cls.initialize_assistant()
            
            # Get response from assistant
            response_text = ""
            status = "failed"
            if ASSISTANT_AVAILABLE and AISingleton.is_initialized():
                try:
                    assistant = get_ai_assistant()
                    assistant.question = question
                    assistant.process_command(question)
                    assistant.answer()
                    if assistant.response is not None:
                        status =  "answered"
                    response_text = assistant.response or "I'm not sure how to respond to that."
                except Exception as e:
                    response_text = f"Sorry, I encountered an error: {str(e)}"
                    status = "failed"
            else:
                response_text = "Assistant is not available at the moment."
            end_time = datetime.now()
            response_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # Save to database if user_id is provided
            if user_id:
                question_response = QuestionResponse(
                    user_id=user_id,
                    question=question,
                    response=response_text,
                    response_time_ms=response_time_ms,
                    status=status,
                    ai_provider=assistant.ai_provider.name if assistant else None
                )
                DatabaseHelper.save(question_response)
            
            # Create response DTO
            response_dto = AskQuestionResponseDTO(
                question=question,
                response=response_text,
                response_time_ms=response_time_ms,
                timestamp=datetime.now().isoformat(),
                user_id=user_id,
                ai_provider=assistant.ai_provider.name if assistant else None,
                status=status
            )
            
            return ResponseHandler.success('Question processed successfully', response_dto.to_dict())
            
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
            
            # Use DTO for query parameters
            try:
                query_dto = ConversationQueryDTO.from_dict(query_params)
                is_valid, error_msg = query_dto.validate()
                if not is_valid:
                    return ResponseHandler.validation_error(error_msg)
            except ValueError as e:
                return ResponseHandler.validation_error(str(e))
            
            conversations = QuestionResponse.query.filter_by(user_id=user_id)\
                .order_by(QuestionResponse.timestamp.desc())\
                .limit(query_dto.limit)\
                .offset(query_dto.offset)\
                .all()
            
            total = QuestionResponse.query.filter_by(user_id=user_id).count()
            
            # Create response DTO
            response_dto = ConversationResponseDTO.from_data(
                user=user,
                conversations=conversations,
                total=total,
                limit=query_dto.limit,
                offset=query_dto.offset
            )
            
            return ResponseHandler.success('Conversation history retrieved successfully', response_dto.to_dict())
            
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @classmethod
    def get_assistant_status(cls):
        """Get current assistant status"""
        try:
            assistant = get_ai_assistant() if AISingleton.is_initialized() else None
            
            # Create status DTO
            status_dto = AssistantStatusDTO(
                available=ASSISTANT_AVAILABLE,
                initialized=AISingleton.is_initialized(),
                name=assistant.name if assistant else None,
                is_connected=assistant.is_connected() if assistant else False,
                ai_provider=assistant.ai_provider.name if assistant else None,
                response_time=assistant.ai_provider.response_time if assistant else None
            )
            
            return ResponseHandler.success('Assistant status retrieved successfully', status_dto.to_dict())
            
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @classmethod
    def reset_assistant(cls):
        """Reset assistant conversation state"""
        try:
            if not ASSISTANT_AVAILABLE or not AISingleton.is_initialized():
                return ResponseHandler.error('Assistant not available', 503)
            
            # Reset assistant state if method exists
            assistant = get_ai_assistant()
            if hasattr(assistant, 'reset_conversation'):
                assistant.reset_conversation()
            
            return ResponseHandler.success('Assistant conversation reset successfully', {
                'status': 'reset'
            })
            
        except Exception as e:
            return ResponseHandler.server_error(str(e))
