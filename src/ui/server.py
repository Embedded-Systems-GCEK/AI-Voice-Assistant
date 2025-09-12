from flask import request, jsonify
from utils.helpers import init_cors, check_health
from controllers.user_controller import create_user, get_users, get_user, update_user, delete_user, get_user_questions
from controllers.question_controller import create_question_response, get_question_responses, get_question_response, delete_question_response
from controllers.api_controller import get_example_questions, ask_assistant, get_user_conversation, get_assistant_status, reset_assistant
from models.models import User, QuestionResponse
import threading

init_cors(app)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/health')
def health_check():
    return check_health()

@app.route('/')
def index():
    return "AI Assistant UI Backend"

# Handle preflight OPTIONS requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'status': 'ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET,PUT,POST,DELETE,OPTIONS")
        return response

# User routes
app.add_url_rule('/users', 'create_user', create_user, methods=['POST'])
app.add_url_rule('/users', 'get_users', get_users, methods=['GET'])
app.add_url_rule('/users/<user_id>', 'get_user', get_user, methods=['GET'])
app.add_url_rule('/users/<user_id>', 'update_user', update_user, methods=['PUT'])
app.add_url_rule('/users/<user_id>', 'delete_user', delete_user, methods=['DELETE'])
app.add_url_rule('/users/<user_id>/questions', 'get_user_questions', get_user_questions, methods=['GET'])

# Question routes
app.add_url_rule('/questions', 'create_question_response', create_question_response, methods=['POST'])
app.add_url_rule('/questions', 'get_question_responses', get_question_responses, methods=['GET'])
app.add_url_rule('/questions/<response_id>', 'get_question_response', get_question_response, methods=['GET'])
app.add_url_rule('/questions/<response_id>', 'delete_question_response', delete_question_response, methods=['DELETE'])

# API routes
app.add_url_rule('/api/example-questions', 'get_example_questions', get_example_questions, methods=['GET'])
app.add_url_rule('/api/ask', 'ask_assistant', ask_assistant, methods=['POST'])
app.add_url_rule('/api/conversation/<user_id>', 'get_user_conversation', get_user_conversation, methods=['GET'])
app.add_url_rule('/api/assistant/status', 'get_assistant_status', get_assistant_status, methods=['GET'])
app.add_url_rule('/api/assistant/reset', 'reset_assistant', reset_assistant, methods=['POST'])

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        total_questions = QuestionResponse.query.count()
        
        avg_confidence = db.session.query(db.func.avg(QuestionResponse.confidence_score)).scalar()
        
        avg_response_time = db.session.query(db.func.avg(QuestionResponse.response_time_ms)).scalar()
        
        return jsonify({
            'total_users': total_users,
            'active_users': active_users,
            'total_questions': total_questions,
            'average_confidence_score': round(avg_confidence, 2) if avg_confidence else None,
            'average_response_time_ms': round(avg_response_time, 2) if avg_response_time else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()