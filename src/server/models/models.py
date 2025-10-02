from ..config.config import db
from datetime import datetime
import uuid
from typing import Optional

class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relationship to question responses
    question_responses = db.relationship('QuestionResponse', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
    
    def to_dict(self):
        """Convert user instance to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class QuestionResponse(db.Model):
    """Question response model for storing Q&A interactions"""
    __tablename__ = 'question_responses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    response_time_ms = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='answered')  # e.g., 'answered', 'failed'
    ai_provider= db.Column(db.String(50), nullable=True)  # e.g., 'Ollama', 'OpenAI' 

    def __init__(self, user_id: str, question: str, response: str, status: str = 'answered', response_time_ms: Optional[int] = None, ai_provider: Optional[str] = None):
        self.user_id = user_id
        self.question = question
        self.response = response
        self.response_time_ms = response_time_ms
        self.status = status
        self.ai_provider = ai_provider
        
    def to_dict(self):
        """Convert question response instance to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question': self.question,
            'response': self.response,
            'timestamp': self.timestamp.isoformat(),
            'response_time_ms': self.response_time_ms,
            'status': self.status
        }
    
    def __repr__(self):
        return f'<QuestionResponse {self.id}>'
