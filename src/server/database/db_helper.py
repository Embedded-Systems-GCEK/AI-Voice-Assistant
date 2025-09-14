from config.config import db
from typing import Optional, List, Dict, Any

class DatabaseHelper:
    """Helper class for database operations"""
    
    @staticmethod
    def create_all():
        """Create all database tables"""
        try:
            db.create_all()
            return True
        except Exception as e:
            print(f"Error creating database tables: {e}")
            return False
    
    @staticmethod
    def drop_all():
        """Drop all database tables"""
        try:
            db.drop_all()
            return True
        except Exception as e:
            print(f"Error dropping database tables: {e}")
            return False
    
    @staticmethod
    def save(instance):
        """Save an instance to the database"""
        try:
            db.session.add(instance)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to database: {e}")
            return False
    
    @staticmethod
    def delete(instance):
        """Delete an instance from the database"""
        try:
            db.session.delete(instance)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting from database: {e}")
            return False
    
    @staticmethod
    def commit():
        """Commit current transaction"""
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error committing transaction: {e}")
            return False
    
    @staticmethod
    def rollback():
        """Rollback current transaction"""
        try:
            db.session.rollback()
            return True
        except Exception as e:
            print(f"Error rolling back transaction: {e}")
            return False
    
    @staticmethod
    def get_stats() -> Dict[str, Any]:
        """Get database statistics"""
        try:
            from models.models import User, QuestionResponse
            
            total_users = User.query.count()
            active_users = User.query.filter_by(is_active=True).count()
            total_questions = QuestionResponse.query.count()
            
            avg_confidence = db.session.query(db.func.avg(QuestionResponse.confidence_score)).scalar()
            avg_response_time = db.session.query(db.func.avg(QuestionResponse.response_time_ms)).scalar()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_questions': total_questions,
                'average_confidence_score': round(avg_confidence, 2) if avg_confidence else None,
                'average_response_time_ms': round(avg_response_time, 2) if avg_response_time else None
            }
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}
