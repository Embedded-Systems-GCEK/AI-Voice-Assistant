from config.config import app, db
from utils.helpers import init_cors, check_health
from controllers.user_controller import UserController
from controllers.question_controller import QuestionController
from controllers.api_controller import APIController
from handlers.request_handler import CORSHandler
from database.db_helper import DatabaseHelper
from models.models import User, QuestionResponse
import threading

# Initialize CORS
init_cors(app)

# Create database tables
with app.app_context():
    DatabaseHelper.create_all()

# Routes
@app.route('/health')
def health_check():
    return check_health()

@app.route('/')
def index():
    return "AI Assistant Server Backend"

# Handle preflight OPTIONS requests
@app.before_request
def handle_preflight():
    return CORSHandler.handle_preflight()

# User routes
@app.route('/users', methods=['POST'])
def create_user():
    return UserController.create_user()

@app.route('/users', methods=['GET'])
def get_users():
    return UserController.get_users()

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    return UserController.update_user(user_id)

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.delete_user(user_id)

@app.route('/users/<user_id>/questions', methods=['GET'])
def get_user_questions(user_id):
    return UserController.get_user_questions(user_id)

# Question routes
@app.route('/questions', methods=['POST'])
def create_question_response():
    return QuestionController.create_question_response()

@app.route('/questions', methods=['GET'])
def get_question_responses():
    return QuestionController.get_question_responses()

@app.route('/questions/<response_id>', methods=['GET'])
def get_question_response(response_id):
    return QuestionController.get_question_response(response_id)

@app.route('/questions/<response_id>', methods=['DELETE'])
def delete_question_response(response_id):
    return QuestionController.delete_question_response(response_id)

# API routes
@app.route('/api/example-questions', methods=['GET'])
def get_example_questions():
    return APIController.get_example_questions()

@app.route('/api/ask', methods=['POST'])
def ask_assistant():
    return APIController.ask_assistant()

@app.route('/api/conversation/<user_id>', methods=['GET'])
def get_user_conversation(user_id):
    return APIController.get_user_conversation(user_id)

@app.route('/api/assistant/status', methods=['GET'])
def get_assistant_status():
    return APIController.get_assistant_status()

@app.route('/api/assistant/reset', methods=['POST'])
def reset_assistant():
    return APIController.reset_assistant()

# Stats route
@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        stats = DatabaseHelper.get_stats()
        from handlers.request_handler import ResponseHandler
        return ResponseHandler.success('Statistics retrieved successfully', stats)
    except Exception as e:
        from handlers.request_handler import ResponseHandler
        return ResponseHandler.server_error(str(e))

if __name__ == '__main__':
    print("Starting AI Assistant Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)