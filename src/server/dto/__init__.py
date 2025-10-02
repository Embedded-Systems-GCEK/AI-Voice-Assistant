"""
Data Transfer Objects (DTOs) for API request/response validation
"""

from .request_dto import (
    AskQuestionDTO,
    CreateUserDTO,
    UpdateUserDTO,
    CreateQuestionResponseDTO,
    ConversationQueryDTO
)

from .response_dto import (
    UserResponseDTO,
    QuestionResponseDTO,
    ConversationResponseDTO,
    AssistantStatusDTO,
    ExampleQuestionDTO
)

__all__ = [
    # Request DTOs
    'AskQuestionDTO',
    'CreateUserDTO',
    'UpdateUserDTO',
    'CreateQuestionResponseDTO',
    'ConversationQueryDTO',
    
    # Response DTOs
    'UserResponseDTO',
    'QuestionResponseDTO',
    'ConversationResponseDTO',
    'AssistantStatusDTO',
    'ExampleQuestionDTO'
]
