from flask import request, jsonify
from models.models import QuestionResponse, db

def create_question_response():
    try:
        data = request.get_json()
        if not data or 'user_id' not in data or 'question' not in data or 'response' not in data:
            return jsonify({'error': 'user_id, question, and response are required'}), 400
        
        # Verify user exists
        from models.models import User
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        new_response = QuestionResponse(
            user_id=data['user_id'],
            question=data['question'],
            response=data['response'],
            confidence_score=data.get('confidence_score'),
            response_time_ms=data.get('response_time_ms')
        )
        
        db.session.add(new_response)
        db.session.commit()
        
        return jsonify({
            'message': 'Question response created successfully',
            'response': new_response.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_question_responses():
    try:
        user_id = request.args.get('user_id')
        if user_id:
            # Filter by user_id
            user_responses = QuestionResponse.query.filter_by(user_id=user_id).all()
            return jsonify({
                'question_responses': [qr.to_dict() for qr in user_responses]
            }), 200
        else:
            # Return all responses
            all_responses = QuestionResponse.query.all()
            return jsonify({
                'question_responses': [qr.to_dict() for qr in all_responses]
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_question_response(response_id):
    try:
        response = QuestionResponse.query.get(response_id)
        if not response:
            return jsonify({'error': 'Question response not found'}), 404
        
        return jsonify({
            'response': response.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_question_response(response_id):
    try:
        response = QuestionResponse.query.get(response_id)
        if not response:
            return jsonify({'error': 'Question response not found'}), 404
        
        db.session.delete(response)
        db.session.commit()
        
        return jsonify({
            'message': 'Question response deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
