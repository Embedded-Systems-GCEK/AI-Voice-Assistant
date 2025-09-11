from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_assistant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Configuration settings
class Config:
    """Application configuration class"""
    SECRET_KEY = 'dev-secret-key'  # Change this in production
    DATABASE_URL = 'sqlite:///ai_assistant.db'
    CORS_ORIGINS = ["http://localhost:*", "http://127.0.0.1:*"]
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
