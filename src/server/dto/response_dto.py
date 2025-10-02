"""
Response Data Transfer Objects (DTOs)
Used for structuring outgoing API response data
"""

from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class UserResponseDTO:
    """DTO for user response"""
    id: str
    username: str
    email: str
    created_at: str
    is_active: bool
    name: Optional[str] = None
    updated_at: Optional[str] = None
    
    @classmethod
    def from_model(cls, user) -> 'UserResponseDTO':
        """Create DTO from User model"""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at.isoformat(),
            is_active=user.is_active,
            name=getattr(user, 'name', None),
            updated_at=user.updated_at.isoformat() if hasattr(user, 'updated_at') and user.updated_at else None
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        # Remove None values for cleaner response
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class QuestionResponseDTO:
    """DTO for question-response data"""
    id: str
    user_id: str
    question: str
    response: str
    timestamp: str
    confidence_score: Optional[float] = None
    response_time_ms: Optional[int] = None
    status: Optional[str] = None
    ai_provider: Optional[str] = None
    
    @classmethod
    def from_model(cls, question_response) -> 'QuestionResponseDTO':
        """Create DTO from QuestionResponse model"""
        return cls(
            id=question_response.id,
            user_id=question_response.user_id,
            question=question_response.question,
            response=question_response.response,
            timestamp=question_response.timestamp.isoformat(),
            confidence_score=question_response.confidence_score,
            response_time_ms=question_response.response_time_ms,
            status=getattr(question_response, 'status', None),
            ai_provider=getattr(question_response, 'ai_provider', None)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        # Remove None values for cleaner response
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ConversationResponseDTO:
    """DTO for conversation history response"""
    user: Dict[str, Any]
    conversations: List[Dict[str, Any]]
    total: int
    limit: int
    offset: int
    
    @classmethod
    def from_data(cls, user, conversations: List, total: int, limit: int, offset: int) -> 'ConversationResponseDTO':
        """Create DTO from conversation data"""
        return cls(
            user=UserResponseDTO.from_model(user).to_dict(),
            conversations=[QuestionResponseDTO.from_model(conv).to_dict() for conv in conversations],
            total=total,
            limit=limit,
            offset=offset
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class AssistantStatusDTO:
    """DTO for assistant status response"""
    available: bool
    initialized: bool
    name: Optional[str] = None
    is_connected: bool = False
    ai_provider: Optional[str] = None
    response_time: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        # Remove None values for cleaner response
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ExampleQuestionDTO:
    """DTO for example question"""
    id: int
    category: str
    question: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class AskQuestionResponseDTO:
    """DTO for ask question response"""
    question: str
    response: str
    response_time_ms: int
    timestamp: str
    user_id: Optional[str] = None
    ai_provider: Optional[str] = None
    status: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        # Remove None values for cleaner response
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class PaginatedResponseDTO:
    """Generic DTO for paginated responses"""
    items: List[Dict[str, Any]]
    total: int
    limit: int
    offset: int
    has_more: bool
    
    @classmethod
    def from_data(cls, items: List, total: int, limit: int, offset: int) -> 'PaginatedResponseDTO':
        """Create paginated response"""
        has_more = (offset + limit) < total
        return cls(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
            has_more=has_more
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
