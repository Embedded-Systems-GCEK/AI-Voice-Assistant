from flask import jsonify
from flask_cors import CORS

def init_cors(app):
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:*", "http://127.0.0.1:*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
        }
    })

def check_health():
    return jsonify({'status': 'healthy', 'timestamp': '2023-01-01T00:00:00Z'})  # Placeholder
