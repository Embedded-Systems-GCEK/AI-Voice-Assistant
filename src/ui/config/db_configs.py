# Database configuration
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
def get_db(app: Flask) -> SQLAlchemy:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_assistant.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    return db