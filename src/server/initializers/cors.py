from flask_cors import CORS

# Enable CORS for all routes

def init_cors(app):
	CORS(app, resources={
		r"/*": {
			"origins": ["http://localhost:*", "http://127.0.0.1:*"],
			"methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
			"allow_headers": ["Content-Type", "Authorization", "Accept"],
		}
	})