from .config.config import app
from .utils.helpers import init_cors, check_health
from .controllers.user_controller import UserController
from .controllers.question_controller import QuestionController
from .controllers.api_controller import APIController
from .handlers.request_handler import CORSHandler
from .database.db_helper import DatabaseHelper
from .models.models import User, QuestionResponse

from .handlers.request_handler import ResponseHandler


# Logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Views
from .views import index_page

# assistant
from ai_assistant import ai_singleton


# Initialize CORS
init_cors(app)

# Create database tables
with app.app_context():
    DatabaseHelper.create_all()


# check if the ai assistant is initialized, if not initialize it

if ai_singleton.is_initialized():
    assistant = ai_singleton.get_assistant()
    logger.info("AI Assistant singleton retrieved on server startup")
else:
    ai_singleton.initialize_assistant(name="Minix")
    assistant = ai_singleton.get_assistant()
    logger.info(" AI Assistant singleton initialized on server startup")




# Routes
@app.route('/health')
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Server is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
            timestamp:
              type: string
              format: date-time
    """
    return check_health()

@app.route("/ping")
def ping():
    """
    Simple ping endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: Pong response
        content:
          text/html:
            schema:
              type: string
              example: "<h1>Pong!</h1>"
    """
    return "<h1>Pong!</h1>"




# Handle preflight OPTIONS requests
@app.before_request
def handle_preflight():
    return CORSHandler.handle_preflight()

# User routes
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: user_data
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: The user's name
              example: "John Doe"
            email:
              type: string
              format: email
              description: The user's email address
              example: "john.doe@example.com"
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
            data:
              type: object
              properties:
                id:
                  type: string
                name:
                  type: string
                email:
                  type: string
                created_at:
                  type: string
                  format: date-time
    """
    return UserController.create_user()

@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  name:
                    type: string
                  email:
                    type: string
                  created_at:
                    type: string
                    format: date-time
    """
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
    """
    Get example questions for the assistant
    ---
    tags:
      - API
    responses:
      200:
        description: List of example questions
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  category:
                    type: string
                  question:
                    type: string
                  description:
                    type: string
    """
    return APIController.get_example_questions()

@app.route('/api/ask', methods=['POST'])
def ask_assistant():
    """
    Ask a question to the AI assistant
    ---
    tags:
      - API
    parameters:
      - in: body
        name: question_data
        required: true
        schema:
          type: object
          required:
            - question
          properties:
            question:
              type: string
              description: The question to ask the assistant
              example: "What time is it?"
            user_id:
              type: string
              description: Optional user ID for conversation tracking
              example: "user123"
    responses:
      200:
        description: Successful response from assistant
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
            data:
              type: object
              properties:
                question:
                  type: string
                response:
                  type: string
                confidence_score:
                  type: number
                  format: float
                response_time_ms:
                  type: integer
                timestamp:
                  type: string
                  format: date-time
                user_id:
                  type: string
    """
    return APIController.ask_assistant()

@app.route('/api/conversation/<user_id>', methods=['GET'])
def get_user_conversation(user_id):
    """
    Get conversation history for a specific user
    ---
    tags:
      - API
    parameters:
      - in: path
        name: user_id
        required: true
        type: string
        description: The user ID
      - in: query
        name: limit
        type: integer
        description: Maximum number of conversations to return
        default: 50
      - in: query
        name: offset
        type: integer
        description: Number of conversations to skip
        default: 0
    responses:
      200:
        description: User's conversation history
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  user_id:
                    type: string
                  question:
                    type: string
                  response:
                    type: string
                  confidence_score:
                    type: number
                    format: float
                  response_time_ms:
                    type: integer
                  timestamp:
                    type: string
                    format: date-time
      404:
        description: User not found
    """
    return APIController.get_user_conversation(user_id)

@app.route('/api/assistant/status', methods=['GET'])
def get_assistant_status():
    """
    Get the current status of the AI assistant
    ---
    tags:
      - API
    responses:
      200:
        description: Assistant status information
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
            data:
              type: object
              properties:
                name:
                  type: string
                initialized:
                  type: boolean
                provider:
                  type: string
    """
    return APIController.get_assistant_status()

@app.route('/api/assistant/reset', methods=['POST'])
def reset_assistant():
    return APIController.reset_assistant()

# Stats route
@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        stats = DatabaseHelper.get_stats()
        assistant_status = assistant.get_status()
        stats['assistant_status'] = assistant_status
        logger.info("Statistics retrieved successfully")
        return ResponseHandler.success('Statistics retrieved successfully', stats)
    except Exception as e:
        logger.error(f"Error retrieving statistics: {e}")
        return ResponseHandler.server_error(str(e))

if __name__ == '__main__':
    print("Starting AI Assistant Unified Server...")
    print("This server provides both API and UI functionality")
    print("Available on: http://localhost:5000")
    print("API endpoints: http://localhost:5000/api/")
    print("Health check: http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=True)