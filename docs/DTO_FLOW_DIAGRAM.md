# DTO Flow Diagram

## Request Flow with DTOs

```
┌─────────────────────────────────────────────────────────────────┐
│                         API REQUEST                              │
│                                                                  │
│  POST /api/ask                                                   │
│  Content-Type: application/json                                 │
│  {                                                              │
│    "question": "What is AI?",                                   │
│    "user_id": "123"                                             │
│  }                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CONTROLLER (api_controller.py)                  │
│                                                                  │
│  1. Get JSON data                                               │
│     data = RequestHandler.get_json_data()                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               REQUEST DTO (request_dto.py)                       │
│                                                                  │
│  2. Create & Validate DTO                                       │
│     dto = AskQuestionDTO.from_dict(data)                        │
│                                                                  │
│     ┌─────────────────────────────────────┐                    │
│     │ AskQuestionDTO                       │                    │
│     │ ─────────────────                    │                    │
│     │ question: str                        │                    │
│     │ user_id: Optional[str]               │                    │
│     │                                      │                    │
│     │ validate():                          │                    │
│     │   ✓ Question not empty               │                    │
│     │   ✓ Length <= 1000 chars             │                    │
│     │   ✓ User ID format (if provided)     │                    │
│     └─────────────────────────────────────┘                    │
│                                                                  │
│  3. Check validation                                            │
│     is_valid, error_msg = dto.validate()                        │
│     if not is_valid:                                            │
│       return error_response                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ Validated Data
┌─────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC                                │
│                                                                  │
│  4. Use validated data (type-safe)                              │
│     question = dto.question    # str                            │
│     user_id = dto.user_id      # Optional[str]                  │
│                                                                  │
│  5. Process the request                                         │
│     - Initialize AI assistant                                   │
│     - Send question to AI                                       │
│     - Get response                                              │
│     - Calculate response time                                   │
│     - Save to database (if user_id)                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼ Processed Data
┌─────────────────────────────────────────────────────────────────┐
│              RESPONSE DTO (response_dto.py)                      │
│                                                                  │
│  6. Create Response DTO                                         │
│     response_dto = AskQuestionResponseDTO(                      │
│         question=question,                                      │
│         response=ai_response,                                   │
│         response_time_ms=234,                                   │
│         timestamp="2025-10-02T14:30:00.123",                    │
│         user_id=user_id,                                        │
│         ai_provider="cohere",                                   │
│         status="answered"                                       │
│     )                                                           │
│                                                                  │
│  7. Convert to dictionary                                       │
│     data = response_dto.to_dict()                               │
│     # Automatically removes None values                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESPONSE HANDLER                              │
│                                                                  │
│  8. Wrap in standard response                                   │
│     return ResponseHandler.success(                             │
│         'Question processed successfully',                      │
│         data                                                    │
│     )                                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API RESPONSE                              │
│                                                                  │
│  HTTP/1.1 200 OK                                                │
│  Content-Type: application/json                                 │
│  {                                                              │
│    "status": "success",                                         │
│    "message": "Question processed successfully",                │
│    "data": {                                                    │
│      "question": "What is AI?",                                 │
│      "response": "AI is artificial intelligence...",            │
│      "response_time_ms": 234,                                   │
│      "timestamp": "2025-10-02T14:30:00.123456",                 │
│      "user_id": "123",                                          │
│      "ai_provider": "cohere",                                   │
│      "status": "answered"                                       │
│    }                                                            │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Error Flow with DTOs

```
┌─────────────────────────────────────────────────────────────────┐
│                         API REQUEST                              │
│                                                                  │
│  POST /api/ask                                                   │
│  {                                                              │
│    "question": ""  ❌ EMPTY!                                    │
│  }                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CONTROLLER                                 │
│  data = RequestHandler.get_json_data()                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REQUEST DTO                                 │
│                                                                  │
│  dto = AskQuestionDTO.from_dict(data)                           │
│  ✓ Created successfully                                         │
│                                                                  │
│  is_valid, error_msg = dto.validate()                           │
│  ❌ Validation failed!                                          │
│  error_msg = "Question cannot be empty"                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RESPONSE HANDLER                               │
│                                                                  │
│  return ResponseHandler.validation_error(error_msg)             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       ERROR RESPONSE                             │
│                                                                  │
│  HTTP/1.1 400 Bad Request                                       │
│  {                                                              │
│    "status": "error",                                           │
│    "message": "Question cannot be empty"                        │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## DTO Structure Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                           DTO Layer                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────┐          ┌────────────────────┐        │
│  │  REQUEST DTOs       │          │  RESPONSE DTOs      │        │
│  │  ───────────────    │          │  ───────────────    │        │
│  │                     │          │                     │        │
│  │  • Validate input   │          │  • Format output    │        │
│  │  • Parse data       │          │  • Clean data       │        │
│  │  • Type checking    │          │  • Remove None      │        │
│  │  • Error messages   │          │  • Consistency      │        │
│  │                     │          │                     │        │
│  │  Examples:          │          │  Examples:          │        │
│  │  ─────────          │          │  ─────────          │        │
│  │  AskQuestionDTO     │          │  UserResponseDTO    │        │
│  │  CreateUserDTO      │          │  QuestionResponseDTO│        │
│  │  UpdateUserDTO      │          │  ConversationDTO    │        │
│  │  ConversationQuery  │          │  AssistantStatusDTO │        │
│  │                     │          │                     │        │
│  └────────────────────┘          └────────────────────┘        │
│           │                                  ▲                   │
│           │                                  │                   │
│           ▼                                  │                   │
│  ┌──────────────────────────────────────────────┐              │
│  │           CONTROLLER LAYER                    │              │
│  │  ─────────────────────────────                │              │
│  │                                               │              │
│  │  • Uses Request DTOs for input               │              │
│  │  • Processes business logic                  │              │
│  │  • Uses Response DTOs for output             │              │
│  │                                               │              │
│  └──────────────────────────────────────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Validation Flow

```
INPUT DATA
    │
    ▼
┌─────────────────┐
│ from_dict()     │ ──> Parse JSON → Create DTO instance
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ validate()      │ ──> Check all rules
└────────┬────────┘
         │
         ├──> Valid ✓    ──> Continue processing
         │
         └──> Invalid ✗  ──> Return error response
```

## Response Building Flow

```
PROCESSED DATA
    │
    ▼
┌─────────────────┐
│ Create DTO      │ ──> Instantiate with data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ to_dict()       │ ──> Convert to dictionary
└────────┬────────┘     Remove None values
         │
         ▼
┌─────────────────┐
│ ResponseHandler │ ──> Wrap in standard format
└────────┬────────┘
         │
         ▼
    JSON RESPONSE
```

## Validation Rules Visualization

```
┌──────────────────────────────────────────────────────────────┐
│                    AskQuestionDTO                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  question: str                                               │
│  ├─ ✓ Not empty                                              │
│  ├─ ✓ Length <= 1000                                         │
│  └─ ✓ Stripped of whitespace                                 │
│                                                               │
│  user_id: Optional[str]                                      │
│  └─ ⚠ Optional (no validation if None)                       │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                     CreateUserDTO                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  username: str                                               │
│  ├─ ✓ Not empty                                              │
│  ├─ ✓ Length >= 3                                            │
│  ├─ ✓ Length <= 80                                           │
│  └─ ✓ Stripped of whitespace                                 │
│                                                               │
│  email: str                                                  │
│  ├─ ✓ Contains '@'                                           │
│  ├─ ✓ Length <= 120                                          │
│  └─ ✓ Stripped of whitespace                                 │
│                                                               │
│  name: Optional[str]                                         │
│  └─ ⚠ Optional                                               │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                  ConversationQueryDTO                         │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  limit: int (default=50)                                     │
│  ├─ ✓ > 0                                                    │
│  └─ ✓ <= 1000                                                │
│                                                               │
│  offset: int (default=0)                                     │
│  └─ ✓ >= 0                                                   │
│                                                               │
│  category: Optional[str]                                     │
│  └─ ⚠ Optional                                               │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Benefits Summary

```
┌──────────────────────────────────────────────────────────────┐
│                   WITHOUT DTOs                                │
├──────────────────────────────────────────────────────────────┤
│  ❌ Manual validation everywhere                              │
│  ❌ No type safety                                            │
│  ❌ Inconsistent error messages                               │
│  ❌ Hard to test                                              │
│  ❌ Scattered validation logic                                │
│  ❌ Duplicate code                                            │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼ REFACTOR TO DTOs
┌──────────────────────────────────────────────────────────────┐
│                     WITH DTOs                                 │
├──────────────────────────────────────────────────────────────┤
│  ✅ Centralized validation                                    │
│  ✅ Full type safety                                          │
│  ✅ Consistent error messages                                 │
│  ✅ Easy to unit test                                         │
│  ✅ Single source of truth                                    │
│  ✅ DRY (Don't Repeat Yourself)                               │
│  ✅ Self-documenting code                                     │
│  ✅ Clean response format                                     │
└──────────────────────────────────────────────────────────────┘
```
