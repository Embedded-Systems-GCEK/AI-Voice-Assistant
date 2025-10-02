# Data Transfer Objects (DTOs) Implementation Guide

## Overview

DTOs (Data Transfer Objects) are used to structure and validate data flowing in and out of the API. They provide:

- ✅ **Type Safety**: Clear data structures with type hints
- ✅ **Validation**: Built-in validation logic
- ✅ **Documentation**: Self-documenting code
- ✅ **Consistency**: Standardized data formats
- ✅ **Testability**: Easy to test and mock

## Architecture

```
dto/
├── __init__.py           # Public API exports
├── request_dto.py        # Incoming request DTOs
└── response_dto.py       # Outgoing response DTOs
```

## Request DTOs

Request DTOs validate and structure incoming API data.

### AskQuestionDTO

Used for: `POST /api/ask`

**Purpose**: Validate question requests to the AI assistant

**Fields**:
- `question` (str, required): The question to ask
- `user_id` (str, optional): User identifier for tracking

**Example**:
```python
from dto.request_dto import AskQuestionDTO

# In controller
data = RequestHandler.get_json_data()
dto = AskQuestionDTO.from_dict(data)

# Validate
is_valid, error_msg = dto.validate()
if not is_valid:
    return ResponseHandler.validation_error(error_msg)

# Use validated data
question = dto.question
user_id = dto.user_id
```

**Validation Rules**:
- Question cannot be empty
- Question max length: 1000 characters
- User ID is optional

---

### CreateUserDTO

Used for: `POST /users`

**Purpose**: Validate user creation requests

**Fields**:
- `username` (str, required): Unique username
- `email` (str, required): User email address
- `name` (str, optional): Full name

**Example**:
```python
from dto.request_dto import CreateUserDTO

dto = CreateUserDTO.from_dict(data)
is_valid, error_msg = dto.validate()
```

**Validation Rules**:
- Username: 3-80 characters
- Email: Must contain '@' and be max 120 characters
- Name: Optional

---

### UpdateUserDTO

Used for: `PUT /users/<user_id>`

**Purpose**: Validate user update requests

**Fields**:
- `username` (str, optional): Updated username
- `email` (str, optional): Updated email
- `name` (str, optional): Updated full name
- `is_active` (bool, optional): Account status

**Example**:
```python
from dto.request_dto import UpdateUserDTO

dto = UpdateUserDTO.from_dict(data)

# Check if there are any updates
if not dto.has_updates():
    return ResponseHandler.validation_error('No updates provided')

# Validate
is_valid, error_msg = dto.validate()
```

---

### CreateQuestionResponseDTO

Used for: `POST /questions`

**Purpose**: Manually create question-response records

**Fields**:
- `user_id` (str, required)
- `question` (str, required)
- `response` (str, required)
- `confidence_score` (float, optional): 0.0 to 1.0
- `response_time_ms` (int, optional): Response time in milliseconds

**Validation Rules**:
- Confidence score: Between 0 and 1
- Response time: Cannot be negative

---

### ConversationQueryDTO

Used for: `GET /api/conversation/<user_id>`

**Purpose**: Validate pagination and filtering parameters

**Fields**:
- `limit` (int, default=50): Max records to return
- `offset` (int, default=0): Records to skip
- `category` (str, optional): Filter by category

**Validation Rules**:
- Limit: 1 to 1000
- Offset: >= 0

---

## Response DTOs

Response DTOs structure outgoing API data.

### UserResponseDTO

**Purpose**: Structure user data in responses

**Fields**:
- `id` (str)
- `username` (str)
- `email` (str)
- `created_at` (str): ISO 8601 format
- `is_active` (bool)
- `name` (str, optional)
- `updated_at` (str, optional)

**Example**:
```python
from dto.response_dto import UserResponseDTO

user = User.query.get(user_id)
dto = UserResponseDTO.from_model(user)
return ResponseHandler.success('User retrieved', dto.to_dict())
```

---

### QuestionResponseDTO

**Purpose**: Structure question-response data

**Fields**:
- `id` (str)
- `user_id` (str)
- `question` (str)
- `response` (str)
- `timestamp` (str)
- `confidence_score` (float, optional)
- `response_time_ms` (int, optional)
- `status` (str, optional)
- `ai_provider` (str, optional)

---

### AskQuestionResponseDTO

**Purpose**: Response for asking questions to AI

**Fields**:
- `question` (str)
- `response` (str)
- `response_time_ms` (int)
- `timestamp` (str)
- `user_id` (str, optional)
- `ai_provider` (str, optional)
- `status` (str, optional)

**Example**:
```python
from dto.response_dto import AskQuestionResponseDTO

response_dto = AskQuestionResponseDTO(
    question=question,
    response=response_text,
    response_time_ms=234,
    timestamp=datetime.now().isoformat(),
    user_id=user_id,
    ai_provider="cohere",
    status="answered"
)

return ResponseHandler.success('Question processed', response_dto.to_dict())
```

---

### ConversationResponseDTO

**Purpose**: Response with conversation history

**Fields**:
- `user` (dict): User information
- `conversations` (list): List of conversations
- `total` (int): Total conversation count
- `limit` (int): Current page limit
- `offset` (int): Current offset

**Example**:
```python
from dto.response_dto import ConversationResponseDTO

response_dto = ConversationResponseDTO.from_data(
    user=user,
    conversations=conversations,
    total=total,
    limit=50,
    offset=0
)

return ResponseHandler.success('History retrieved', response_dto.to_dict())
```

---

### AssistantStatusDTO

**Purpose**: AI assistant status information

**Fields**:
- `available` (bool)
- `initialized` (bool)
- `name` (str, optional)
- `is_connected` (bool)
- `ai_provider` (str, optional)
- `response_time` (float, optional)

---

### PaginatedResponseDTO

**Purpose**: Generic paginated responses

**Fields**:
- `items` (list): List of items
- `total` (int): Total count
- `limit` (int): Page size
- `offset` (int): Current offset
- `has_more` (bool): Whether more items exist

---

## Benefits of Using DTOs

### 1. Type Safety
```python
# Before (no DTOs)
question = data['question']  # Could be None, wrong type, etc.

# After (with DTOs)
dto = AskQuestionDTO.from_dict(data)
question = dto.question  # Type-safe, validated
```

### 2. Validation
```python
# Before
if 'question' not in data:
    return error()
if not data['question']:
    return error()
if len(data['question']) > 1000:
    return error()

# After
is_valid, error_msg = dto.validate()
if not is_valid:
    return ResponseHandler.validation_error(error_msg)
```

### 3. Documentation
```python
# DTOs are self-documenting
@dataclass
class AskQuestionDTO:
    """DTO for ask question endpoint"""
    question: str  # Clear what's expected
    user_id: Optional[str] = None  # Optional field
```

### 4. Testability
```python
# Easy to test
dto = AskQuestionDTO(question="Test?", user_id="123")
is_valid, error = dto.validate()
assert is_valid == True
```

### 5. Consistency
```python
# All responses have consistent structure
response_dto.to_dict()  # Always returns clean dict
# Removes None values automatically
```

---

## Usage in Controllers

### Before (Without DTOs)
```python
def ask_assistant():
    data = RequestHandler.get_json_data()
    
    # Manual validation
    if 'question' not in data:
        return ResponseHandler.validation_error('Missing question')
    
    question = data['question']
    user_id = data.get('user_id')
    
    # ... process ...
    
    # Manual response building
    return ResponseHandler.success('Success', {
        'question': question,
        'response': response_text,
        'response_time_ms': response_time,
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id
    })
```

### After (With DTOs)
```python
def ask_assistant():
    data = RequestHandler.get_json_data()
    
    # DTO handles validation
    try:
        dto = AskQuestionDTO.from_dict(data)
        is_valid, error_msg = dto.validate()
        if not is_valid:
            return ResponseHandler.validation_error(error_msg)
    except ValueError as e:
        return ResponseHandler.validation_error(str(e))
    
    # Use validated data
    question = dto.question
    user_id = dto.user_id
    
    # ... process ...
    
    # DTO structures response
    response_dto = AskQuestionResponseDTO(
        question=question,
        response=response_text,
        response_time_ms=response_time,
        timestamp=datetime.now().isoformat(),
        user_id=user_id
    )
    
    return ResponseHandler.success('Success', response_dto.to_dict())
```

---

## Best Practices

### 1. Always Validate
```python
dto = RequestDTO.from_dict(data)
is_valid, error_msg = dto.validate()
if not is_valid:
    return ResponseHandler.validation_error(error_msg)
```

### 2. Handle Exceptions
```python
try:
    dto = RequestDTO.from_dict(data)
except ValueError as e:
    return ResponseHandler.validation_error(str(e))
```

### 3. Use `to_dict()` for Responses
```python
response_dto = ResponseDTO.from_model(model)
return ResponseHandler.success('Success', response_dto.to_dict())
```

### 4. Keep DTOs Simple
- DTOs should only contain data and validation logic
- No business logic in DTOs
- No database operations in DTOs

### 5. Use Type Hints
```python
from typing import Optional

@dataclass
class MyDTO:
    required_field: str
    optional_field: Optional[int] = None
```

---

## Testing DTOs

### Unit Tests
```python
import pytest
from dto.request_dto import AskQuestionDTO

def test_valid_question():
    dto = AskQuestionDTO(question="Test?", user_id="123")
    is_valid, error = dto.validate()
    assert is_valid == True

def test_empty_question():
    dto = AskQuestionDTO(question="", user_id="123")
    is_valid, error = dto.validate()
    assert is_valid == False
    assert "empty" in error.lower()

def test_from_dict():
    data = {"question": "Test?", "user_id": "123"}
    dto = AskQuestionDTO.from_dict(data)
    assert dto.question == "Test?"
    assert dto.user_id == "123"

def test_missing_required_field():
    with pytest.raises(ValueError):
        AskQuestionDTO.from_dict({})
```

---

## Migration Guide

To add DTOs to an existing endpoint:

1. **Create Request DTO** (if needed)
2. **Create Response DTO** (if needed)
3. **Update Controller**:
   - Import DTOs
   - Replace manual validation with DTO validation
   - Replace manual response building with DTO
4. **Test the endpoint**
5. **Update documentation**

---

## Summary

DTOs provide a clean, maintainable way to handle API data:

- ✅ Request validation
- ✅ Response formatting
- ✅ Type safety
- ✅ Self-documentation
- ✅ Easy testing
- ✅ Consistency across API

All new endpoints should use DTOs for better code quality and maintainability.
