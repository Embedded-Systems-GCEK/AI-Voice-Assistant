"""
Request Data Transfer Objects (DTOs)
Used for validating and structuring incoming API request data
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class AskQuestionDTO:
    """DTO for ask question endpoint"""
    question: str
    user_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AskQuestionDTO':
        """Create DTO from dictionary"""
        if not data:
            raise ValueError("Request data cannot be empty")
        
        if 'question' not in data:
            raise ValueError("Missing required field: 'question'")
        
        if not data['question'] or not data['question'].strip():
            raise ValueError("Question cannot be empty")
        
        return cls(
            question=data['question'].strip(),
            user_id=data.get('user_id')
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the DTO"""
        if not self.question or len(self.question.strip()) == 0:
            return False, "Question cannot be empty"
        
        if len(self.question) > 1000:
            return False, "Question is too long (max 1000 characters)"
        
        return True, None


@dataclass
class CreateUserDTO:
    """DTO for creating a new user"""
    username: str
    email: str
    name: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CreateUserDTO':
        """Create DTO from dictionary"""
        if not data:
            raise ValueError("Request data cannot be empty")
        
        required_fields = ['username', 'email']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return cls(
            username=data['username'].strip(),
            email=data['email'].strip(),
            name=data.get('name', '').strip() if data.get('name') else None
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the DTO"""
        if not self.username or len(self.username.strip()) == 0:
            return False, "Username cannot be empty"
        
        if len(self.username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(self.username) > 80:
            return False, "Username is too long (max 80 characters)"
        
        if not self.email or '@' not in self.email:
            return False, "Invalid email address"
        
        if len(self.email) > 120:
            return False, "Email is too long (max 120 characters)"
        
        return True, None


@dataclass
class UpdateUserDTO:
    """DTO for updating user information"""
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UpdateUserDTO':
        """Create DTO from dictionary"""
        if not data:
            raise ValueError("Request data cannot be empty")
        
        return cls(
            username=data.get('username', '').strip() if data.get('username') else None,
            email=data.get('email', '').strip() if data.get('email') else None,
            name=data.get('name', '').strip() if data.get('name') else None,
            is_active=data.get('is_active')
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the DTO"""
        if self.username is not None:
            if len(self.username.strip()) == 0:
                return False, "Username cannot be empty"
            if len(self.username) < 3:
                return False, "Username must be at least 3 characters"
            if len(self.username) > 80:
                return False, "Username is too long (max 80 characters)"
        
        if self.email is not None:
            if '@' not in self.email:
                return False, "Invalid email address"
            if len(self.email) > 120:
                return False, "Email is too long (max 120 characters)"
        
        return True, None
    
    def has_updates(self) -> bool:
        """Check if DTO contains any updates"""
        return any([
            self.username is not None,
            self.email is not None,
            self.name is not None,
            self.is_active is not None
        ])


@dataclass
class CreateQuestionResponseDTO:
    """DTO for manually creating a question-response record"""
    user_id: str
    question: str
    response: str
    confidence_score: Optional[float] = None
    response_time_ms: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CreateQuestionResponseDTO':
        """Create DTO from dictionary"""
        if not data:
            raise ValueError("Request data cannot be empty")
        
        required_fields = ['user_id', 'question', 'response']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return cls(
            user_id=data['user_id'],
            question=data['question'].strip(),
            response=data['response'].strip(),
            confidence_score=data.get('confidence_score'),
            response_time_ms=data.get('response_time_ms')
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the DTO"""
        if not self.question or len(self.question.strip()) == 0:
            return False, "Question cannot be empty"
        
        if not self.response or len(self.response.strip()) == 0:
            return False, "Response cannot be empty"
        
        if self.confidence_score is not None:
            if not (0 <= self.confidence_score <= 1):
                return False, "Confidence score must be between 0 and 1"
        
        if self.response_time_ms is not None:
            if self.response_time_ms < 0:
                return False, "Response time cannot be negative"
        
        return True, None


@dataclass
class ConversationQueryDTO:
    """DTO for conversation query parameters"""
    limit: int = 50
    offset: int = 0
    category: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ConversationQueryDTO':
        """Create DTO from query parameters"""
        try:
            limit = int(data.get('limit', 50))
            offset = int(data.get('offset', 0))
        except (ValueError, TypeError):
            raise ValueError("Invalid limit or offset value")
        
        return cls(
            limit=limit,
            offset=offset,
            category=data.get('category')
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate the DTO"""
        if self.limit <= 0:
            return False, "Limit must be greater than 0"
        
        if self.limit > 1000:
            return False, "Limit cannot exceed 1000"
        
        if self.offset < 0:
            return False, "Offset cannot be negative"
        
        return True, None
