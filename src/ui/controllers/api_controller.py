from flask import request, jsonify
from models.models import User, QuestionResponse, db
from datetime import datetime
from api.assistant_api import assistant_instance, ASSISTANT_AVAILABLE, EXAMPLE_QUESTIONS

def get_example_questions():
    """Get example questions for the Flutter app"""
    try:
        category = request.args.get('category')
        if category:
            filtered_questions = [q for q in EXAMPLE_QUESTIONS if q['category'].lower() == category.lower()]
            return jsonify({
                'questions': filtered_questions,
                'total': len(filtered_questions)
            }), 200
        
        return jsonify({
            'questions': EXAMPLE_QUESTIONS,
            'total': len(EXAMPLE_QUESTIONS),
            'categories': list(set(q['category'] for q in EXAMPLE_QUESTIONS))
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def ask_assistant():
    """Ask a question to the AI assistant"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400
        
        question = data['question']
        user_id = data.get('user_id')
        
        # Verify user exists if user_id is provided
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
        
        start_time = datetime.now()
        
        # Get response from assistant
        response_text = ""
        confidence_score = None
        
        if ASSISTANT_AVAILABLE and assistant_instance:
            try:
                # Use assistant to process the question
                assistant_instance.question = question
                assistant_instance.process_command(question)
                response_text = assistant_instance.response or "I'm not sure how to respond to that."
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
            db.session.add(question_response)
            db.session.commit()
        
        return jsonify({
            'question': question,
            'response': response_text,
            'confidence_score': confidence_score,
            'response_time_ms': response_time_ms,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_user_conversation(user_id):
    """Get conversation history for a specific user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        conversations = QuestionResponse.query.filter_by(user_id=user_id)\
            .order_by(QuestionResponse.timestamp.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        return jsonify({
            'user': user.to_dict(),
            'conversations': [conv.to_dict() for conv in conversations],
            'total': QuestionResponse.query.filter_by(user_id=user_id).count()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_assistant_status():
    """Get current assistant status"""
    try:
        status_info = {
            'available': ASSISTANT_AVAILABLE,
            'initialized': assistant_instance is not None,
            'name': assistant_instance.name if assistant_instance else None,
            'timeout_seconds': assistant_instance.timeout_seconds if assistant_instance else None,
            'conversation_state': assistant_instance.conversation_state if assistant_instance else None,
            'user_name': assistant_instance.user_name if assistant_instance else None,
            'is_connected': assistant_instance.is_connected() if assistant_instance else False
        }
        
        return jsonify(status_info), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def reset_assistant():
    """Reset assistant conversation state"""
    try:
        if not ASSISTANT_AVAILABLE or not assistant_instance:
            return jsonify({'error': 'Assistant not available'}), 503
        
        assistant_instance.reset_conversation()
        
        return jsonify({
            'message': 'Assistant conversation reset successfully',
            'status': 'reset'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
