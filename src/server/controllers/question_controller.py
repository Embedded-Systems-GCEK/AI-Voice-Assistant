from ..models.models import User, QuestionResponse
from ..database.db_helper import DatabaseHelper
from ..handlers.request_handler import RequestHandler, ResponseHandler

from ..models.models import User, QuestionResponse
from ..database.db_helper import DatabaseHelper
from ..handlers.request_handler import RequestHandler, ResponseHandler
from ..dto.response_dto import (
    ExampleQuestionDTO
)


try:
    from ai_assistant import get_ai_assistant, initialize_ai_assistant, AISingleton
    ASSISTANT_AVAILABLE = True
except ImportError:
    ASSISTANT_AVAILABLE = False
    raise ImportError("Assistant modules not available")

    
class QuestionController:
    """Controller for handling question response operations"""
    # Example questions for the Flutter app
    def __init__(self):
        self.assistant = get_ai_assistant()
    @staticmethod
    def create_question_response():
        """Create a new question response"""
        try:
            data = RequestHandler.get_json_data()
            
            # Validate required fields
            is_valid, error_msg = RequestHandler.validate_required_fields(data, ['user_id', 'question', 'response'])
            if not is_valid:
                return ResponseHandler.validation_error(error_msg)
            
            # Verify user exists
            user = User.query.get(data['user_id'])
            if not user:
                return ResponseHandler.not_found('User')
            
            # Create new question response
            new_response = QuestionResponse(
                user_id=data['user_id'],
                question=data['question'],
                response=data['response'],
                confidence_score=data.get('confidence_score'),
                response_time_ms=data.get('response_time_ms')
            )
            
            if DatabaseHelper.save(new_response):
                return ResponseHandler.success('Question response created successfully', {
                    'response': new_response.to_dict()
                }, 201)
            else:
                return ResponseHandler.server_error('Failed to create question response')
                
        except Exception as e:
            DatabaseHelper.rollback()
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def get_question_responses():
        """Get question responses, optionally filtered by user_id"""
        try:
            query_params = RequestHandler.get_query_params()
            user_id = query_params.get('user_id')
            
            if user_id:
                # Filter by user_id
                user_responses = QuestionResponse.query.filter_by(user_id=user_id).all()
                return ResponseHandler.success('Question responses retrieved successfully', {
                    'question_responses': [qr.to_dict() for qr in user_responses]
                })
            else:
                # Return all responses
                all_responses = QuestionResponse.query.all()
                return ResponseHandler.success('Question responses retrieved successfully', {
                    'question_responses': [qr.to_dict() for qr in all_responses]
                })
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def get_question_response(response_id: str):
        """Get a specific question response by ID"""
        try:
            response = QuestionResponse.query.get(response_id)
            if not response:
                return ResponseHandler.not_found('Question response')
            
            return ResponseHandler.success('Question response retrieved successfully', {
                'response': response.to_dict()
            })
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def delete_question_response(response_id: str):
        """Delete a question response"""
        try:
            response = QuestionResponse.query.get(response_id)
            if not response:
                return ResponseHandler.not_found('Question response')
            
            if DatabaseHelper.delete(response):
                return ResponseHandler.success('Question response deleted successfully')
            else:
                return ResponseHandler.server_error('Failed to delete question response')
                
        except Exception as e:
            DatabaseHelper.rollback()
            return ResponseHandler.server_error(str(e))
    # @staticmethod
    def get_example_questions(self):
        """Get example questions for the Flutter app"""
        try:
            query_params = RequestHandler.get_query_params()
            category = query_params.get('category')
            
            # Convert to DTOs
            question_dtos = [ExampleQuestionDTO(**q) for q in self.assistant.get_example_questions()]
            
            if category:
                filtered_dtos = [dto for dto in question_dtos 
                                if dto.category.lower() == category.lower()]
                return ResponseHandler.success('Example questions retrieved successfully', {
                    'questions': [dto.to_dict() for dto in filtered_dtos],
                    'total': len(filtered_dtos)
                })
            
            return ResponseHandler.success('Example questions retrieved successfully', {
                'questions': [dto.to_dict() for dto in question_dtos],
                'total': len(question_dtos),
                'categories': list(set(q['category'] for q in self.assistant.get_example_questions()))
            })
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    