from flask import request, jsonify
from models.models import User, QuestionResponse, db
from datetime import datetime
from api.assistant_api import assistant_instance, ASSISTANT_AVAILABLE, EXAMPLE_QUESTIONS

def create_user():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Username and email are required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Check if username already exists
        existing_username = User.query.filter_by(username=data['username']).first()
        if existing_username:
            return jsonify({'error': 'Username already exists'}), 409
        
        from models.models import User
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': new_user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_users():
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'username' in data:
            # Check if username is already taken by another user
            existing_user = User.query.filter(User.username == data['username'], User.id != user_id).first()
            if existing_user:
                return jsonify({'error': 'Username already exists'}), 409
            user.username = data['username']
        
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing_user:
                return jsonify({'error': 'Email already exists'}), 409
            user.email = data['email']
        
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_user_questions(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        responses = QuestionResponse.query.filter_by(user_id=user_id).order_by(QuestionResponse.timestamp.desc()).all()
        
        return jsonify({
            'user': user.to_dict(),
            'question_responses': [response.to_dict() for response in responses],
            'total_responses': len(responses)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
