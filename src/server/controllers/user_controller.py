from ..models.models import User, QuestionResponse
from ..database.db_helper import DatabaseHelper
from ..handlers.request_handler import RequestHandler, ResponseHandler
from typing import Dict, Any

class UserController:
    """Controller for handling user-related operations"""
    
    @staticmethod
    def create_user():
        """Create a new user"""
        try:
            data = RequestHandler.get_json_data()
            
            # Validate required fields
            is_valid, error_msg = RequestHandler.validate_required_fields(data, ['username', 'email'])
            if not is_valid:
                return ResponseHandler.validation_error(error_msg)
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return ResponseHandler.conflict('User with this email already exists')
            
            # Check if username already exists
            existing_username = User.query.filter_by(username=data['username']).first()
            if existing_username:
                return ResponseHandler.conflict('Username already exists')
            
            # Create new user
            new_user = User(username=data['username'], email=data['email'])
            
            if DatabaseHelper.save(new_user):
                return ResponseHandler.success('User created successfully', {'user': new_user.to_dict()}, 201)
            else:
                return ResponseHandler.server_error('Failed to create user')
                
        except Exception as e:
            DatabaseHelper.rollback()
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def get_users():
        """Get all users"""
        try:
            users = User.query.all()
            return ResponseHandler.success('Users retrieved successfully', {
                'users': [user.to_dict() for user in users]
            })
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def get_user(user_id: str):
        """Get a specific user by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                return ResponseHandler.not_found('User')
            
            return ResponseHandler.success('User retrieved successfully', {
                'user': user.to_dict()
            })
        except Exception as e:
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def update_user(user_id: str):
        """Update a user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return ResponseHandler.not_found('User')
            
            data = RequestHandler.get_json_data()
            if not data:
                return ResponseHandler.validation_error('No data provided')
            
            # Update username if provided
            if 'username' in data:
                existing_user = User.query.filter(User.username == data['username'], User.id != user_id).first()
                if existing_user:
                    return ResponseHandler.conflict('Username already exists')
                user.username = data['username']
            
            # Update email if provided
            if 'email' in data:
                existing_user = User.query.filter(User.email == data['email'], User.id != user_id).first()
                if existing_user:
                    return ResponseHandler.conflict('Email already exists')
                user.email = data['email']
            
            # Update active status if provided
            if 'is_active' in data:
                user.is_active = bool(data['is_active'])
            
            if DatabaseHelper.commit():
                return ResponseHandler.success('User updated successfully', {'user': user.to_dict()})
            else:
                return ResponseHandler.server_error('Failed to update user')
                
        except Exception as e:
            DatabaseHelper.rollback()
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def delete_user(user_id: str):
        """Delete a user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return ResponseHandler.not_found('User')
            
            if DatabaseHelper.delete(user):
                return ResponseHandler.success('User deleted successfully')
            else:
                return ResponseHandler.server_error('Failed to delete user')
                
        except Exception as e:
            DatabaseHelper.rollback()
            return ResponseHandler.server_error(str(e))
    
    @staticmethod
    def get_user_questions(user_id: str):
        """Get all questions for a specific user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return ResponseHandler.not_found('User')
            
            responses = QuestionResponse.query.filter_by(user_id=user_id).order_by(QuestionResponse.timestamp.desc()).all()
            
            return ResponseHandler.success('User questions retrieved successfully', {
                'user': user.to_dict(),
                'question_responses': [response.to_dict() for response in responses],
                'total_responses': len(responses)
            })
        except Exception as e:
            return ResponseHandler.server_error(str(e))
