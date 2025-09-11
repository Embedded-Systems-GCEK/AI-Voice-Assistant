from flask_cors import CORS
from flask import jsonify

def init_cors(app):
    """Initialize CORS for the Flask app"""
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:*", "http://127.0.0.1:*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
        }
    })

def check_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Assistant Server is running',
        'timestamp': '2023-01-01T00:00:00Z'  # You can use datetime.now().isoformat()
    })
