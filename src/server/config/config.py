from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../ai_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'AI Voice Assistant API',
    'uiversion': 3,
    'version': '1.0.0',
    'description': 'REST API for AI Voice Assistant with user management and conversation features',
    'termsOfService': None,
    'contact': {
        'name': 'Embedded Systems GCEK',
        'url': 'https://github.com/Embedded-Systems-GCEK'
    }
}

# Initialize database
db = SQLAlchemy(app)

# Initialize Swagger
swagger = Swagger(app)
