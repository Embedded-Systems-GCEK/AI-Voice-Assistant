# AI Voice Assistant - Complete API Guide

## Table of Contents
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Response Format](#response-format)
- [Health & System Endpoints](#health--system-endpoints)
- [User Management Endpoints](#user-management-endpoints)
- [Question Management Endpoints](#question-management-endpoints)
- [AI Assistant Endpoints](#ai-assistant-endpoints)
- [Statistics Endpoints](#statistics-endpoints)
- [Error Handling](#error-handling)
- [Testing Tools](#testing-tools)

---

## Getting Started

### Base URL
```
http://localhost:5000
```

### Interactive Documentation
For interactive testing, visit the Swagger UI:
```
http://localhost:5000/apidocs
```

### Content Type
All POST/PUT requests require:
```
Content-Type: application/json
```

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

> **Note for Production**: Implement authentication before deploying to production.

---

## Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Operation description",
  "data": { /* Response data */ }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description",
  "error": "Detailed error information"
}
```

### HTTP Status Codes
- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST (resource created)
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource
- `500 Internal Server Error` - Server error

---

## Health & System Endpoints

### 1. Health Check

Check if the server is running and healthy.

**Endpoint:** `GET /health`

**cURL:**
```bash
curl -X GET http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-02T14:30:00.123456"
}
```

---

### 2. Ping

Simple connectivity test.

**Endpoint:** `GET /ping`

**cURL:**
```bash
curl -X GET http://localhost:5000/ping
```

**Response:**
```html
<h1>Pong!</h1>
```

---

## User Management Endpoints

### 1. Create User

Create a new user account.

**Endpoint:** `POST /users`

**Required Fields:**
- `username` (string) - Unique username
- `email` (string) - Unique email address

**cURL:**
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "aruncs",
    "email": "arun@example.com"
  }'
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "User created successfully",
  "data": {
    "user": {
      "id": "d5d06cf9-036c-4342-b448-dca4307848c2",
      "username": "aruncs",
      "email": "arun@example.com",
      "created_at": "2025-10-02T14:30:00.123456",
      "is_active": true
    }
  }
}
```

**Error Responses:**
- `400` - Validation error (missing fields)
- `409` - Username or email already exists

---

### 2. Get All Users

Retrieve a list of all registered users.

**Endpoint:** `GET /users`

**cURL:**
```bash
curl -X GET http://localhost:5000/users
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Users retrieved successfully",
  "data": {
    "users": [
      {
        "id": "d5d06cf9-036c-4342-b448-dca4307848c2",
        "username": "aruncs",
        "email": "arun@example.com",
        "created_at": "2025-10-02T14:30:00.123456",
        "is_active": true
      },
      {
        "id": "a1b2c3d4-1234-5678-90ab-cdef12345678",
        "username": "johndoe",
        "email": "john@example.com",
        "created_at": "2025-10-01T10:15:30.456789",
        "is_active": true
      }
    ]
  }
}
```

---

### 3. Get User by ID

Retrieve details of a specific user.

**Endpoint:** `GET /users/{user_id}`

**Path Parameters:**
- `user_id` (string, UUID) - The user's unique identifier

**cURL:**
```bash
curl -X GET http://localhost:5000/users/d5d06cf9-036c-4342-b448-dca4307848c2
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "User retrieved successfully",
  "data": {
    "user": {
      "id": "d5d06cf9-036c-4342-b448-dca4307848c2",
      "username": "aruncs",
      "email": "arun@example.com",
      "created_at": "2025-10-02T14:30:00.123456",
      "is_active": true
    }
  }
}
```

**Error Responses:**
- `404` - User not found

---

### 4. Update User

Update an existing user's information.

**Endpoint:** `PUT /users/{user_id}`

**Path Parameters:**
- `user_id` (string, UUID) - The user's unique identifier

**Optional Fields:**
- `username` (string) - New username
- `email` (string) - New email
- `is_active` (boolean) - Active status

**cURL:**
```bash
curl -X PUT http://localhost:5000/users/d5d06cf9-036c-4342-b448-dca4307848c2 \
  -H "Content-Type: application/json" \
  -d '{
    "username": "arun_cs",
    "email": "arun.new@example.com"
  }'
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "User updated successfully",
  "data": {
    "user": {
      "id": "d5d06cf9-036c-4342-b448-dca4307848c2",
      "username": "arun_cs",
      "email": "arun.new@example.com",
      "created_at": "2025-10-02T14:30:00.123456",
      "is_active": true
    }
  }
}
```

**Error Responses:**
- `404` - User not found
- `409` - Username or email already exists
- `400` - Validation error

---

### 5. Delete User

Delete a user account.

**Endpoint:** `DELETE /users/{user_id}`

**Path Parameters:**
- `user_id` (string, UUID) - The user's unique identifier

**cURL:**
```bash
curl -X DELETE http://localhost:5000/users/d5d06cf9-036c-4342-b448-dca4307848c2
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "User deleted successfully"
}
```

**Error Responses:**
- `404` - User not found

**Note:** Deleting a user will also delete all their question-response records (cascade delete).

---

### 6. Get User's Questions

Retrieve all questions asked by a specific user.

**Endpoint:** `GET /users/{user_id}/questions`

**Path Parameters:**
- `user_id` (string, UUID) - The user's unique identifier

**cURL:**
```bash
curl -X GET http://localhost:5000/users/d5d06cf9-036c-4342-b448-dca4307848c2/questions
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "User questions retrieved successfully",
  "data": [
    {
      "id": "q1a2b3c4-5678-90ab-cdef-1234567890ab",
      "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2",
      "question": "What time is it?",
      "response": "The current time is 2:30 PM",
      "timestamp": "2025-10-02T14:30:00.123456",
      "confidence_score": 0.95,
      "response_time_ms": 234
    }
  ]
}
```

**Error Responses:**
- `404` - User not found

---

## Question Management Endpoints

### 1. Create Question-Response Record

Manually create a question-response record.

**Endpoint:** `POST /questions`

**Required Fields:**
- `user_id` (string, UUID) - User who asked the question
- `question` (string) - The question text
- `response` (string) - The response text

**Optional Fields:**
- `confidence_score` (float, 0-1) - Confidence score
- `response_time_ms` (integer) - Response time in milliseconds

**cURL:**
```bash
curl -X POST http://localhost:5000/questions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2",
    "question": "What is artificial intelligence?",
    "response": "Artificial intelligence is the simulation of human intelligence...",
    "confidence_score": 0.85,
    "response_time_ms": 250
  }'
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "Question response created successfully",
  "data": {
    "id": "q1a2b3c4-5678-90ab-cdef-1234567890ab",
    "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2",
    "question": "What is artificial intelligence?",
    "response": "Artificial intelligence is the simulation of human intelligence...",
    "timestamp": "2025-10-02T14:30:00.123456",
    "confidence_score": 0.85,
    "response_time_ms": 250
  }
}
```

**Error Responses:**
- `400` - Validation error (missing required fields)
- `404` - User not found

---

### 2. Get All Question-Responses

Retrieve all question-response records.

**Endpoint:** `GET /questions`

**Query Parameters:**
- `limit` (integer, optional, default: 100) - Maximum records to return
- `offset` (integer, optional, default: 0) - Number of records to skip

**cURL:**
```bash
# Get all questions
curl -X GET http://localhost:5000/questions

# With pagination
curl -X GET "http://localhost:5000/questions?limit=10&offset=0"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Question responses retrieved successfully",
  "data": [
    {
      "id": "q1a2b3c4-5678-90ab-cdef-1234567890ab",
      "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2",
      "question": "What is AI?",
      "response": "AI is artificial intelligence...",
      "timestamp": "2025-10-02T14:30:00.123456",
      "confidence_score": 0.85,
      "response_time_ms": 250
    }
  ]
}
```

---

### 3. Get Question-Response by ID

Retrieve a specific question-response record.

**Endpoint:** `GET /questions/{response_id}`

**Path Parameters:**
- `response_id` (string, UUID) - The question-response record ID

**cURL:**
```bash
curl -X GET http://localhost:5000/questions/q1a2b3c4-5678-90ab-cdef-1234567890ab
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Question response retrieved successfully",
  "data": {
    "id": "q1a2b3c4-5678-90ab-cdef-1234567890ab",
    "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2",
    "question": "What is AI?",
    "response": "AI is artificial intelligence...",
    "timestamp": "2025-10-02T14:30:00.123456",
    "confidence_score": 0.85,
    "response_time_ms": 250
  }
}
```

**Error Responses:**
- `404` - Question-response not found

---

### 4. Delete Question-Response

Delete a question-response record.

**Endpoint:** `DELETE /questions/{response_id}`

**Path Parameters:**
- `response_id` (string, UUID) - The question-response record ID

**cURL:**
```bash
curl -X DELETE http://localhost:5000/questions/q1a2b3c4-5678-90ab-cdef-1234567890ab
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Question response deleted successfully"
}
```

**Error Responses:**
- `404` - Question-response not found

---

## AI Assistant Endpoints

### 1. Get Example Questions

Retrieve pre-configured example questions.

**Endpoint:** `GET /api/example-questions`

**cURL:**
```bash
curl -X GET http://localhost:5000/api/example-questions
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Example questions retrieved successfully",
  "data": [
    {
      "id": 1,
      "category": "General",
      "question": "What time is it?",
      "description": "Ask for the current time"
    },
    {
      "id": 2,
      "category": "General",
      "question": "What's the date today?",
      "description": "Ask for today's date"
    },
    {
      "id": 3,
      "category": "Knowledge",
      "question": "Tell me about artificial intelligence",
      "description": "Learn about AI"
    }
  ]
}
```

---

### 2. Ask Question to AI Assistant

Ask a question to the AI assistant and get a response.

**Endpoint:** `POST /api/ask`

**Required Fields:**
- `question` (string) - The question to ask

**Optional Fields:**
- `user_id` (string, UUID) - User ID (if provided, saves to database)

**cURL:**
```bash
# Without user_id (not saved to database)
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What time is it?"
  }'

# With user_id (saved to database)
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2"
  }'
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Question processed successfully",
  "data": {
    "question": "What time is it?",
    "response": "The current time is 2:30 PM",
    "confidence_score": 0.95,
    "response_time_ms": 234,
    "timestamp": "2025-10-02T14:30:00.123456",
    "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2"
  }
}
```

**Error Responses:**
- `400` - Validation error (missing question)
- `404` - User not found (if user_id provided)

---

### 3. Get Conversation History

Retrieve conversation history for a specific user.

**Endpoint:** `GET /api/conversation/{user_id}`

**Path Parameters:**
- `user_id` (string, UUID) - The user's unique identifier

**Query Parameters:**
- `limit` (integer, optional, default: 50) - Maximum conversations to return
- `offset` (integer, optional, default: 0) - Number of conversations to skip

**cURL:**
```bash
# Get recent conversations
curl -X GET http://localhost:5000/api/conversation/d5d06cf9-036c-4342-b448-dca4307848c2

# With pagination
curl -X GET "http://localhost:5000/api/conversation/d5d06cf9-036c-4342-b448-dca4307848c2?limit=10&offset=0"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Conversation history retrieved successfully",
  "data": [
    {
      "id": "q1a2b3c4-5678-90ab-cdef-1234567890ab",
      "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2",
      "question": "What is AI?",
      "response": "AI is artificial intelligence...",
      "timestamp": "2025-10-02T14:30:00.123456",
      "confidence_score": 0.85,
      "response_time_ms": 250
    },
    {
      "id": "q2b3c4d5-6789-01ab-cdef-234567890abc",
      "user_id": "d5d06cf9-036c-4342-b448-dca4307848c2",
      "question": "Tell me more",
      "response": "AI includes machine learning...",
      "timestamp": "2025-10-02T14:31:15.789012",
      "confidence_score": 0.82,
      "response_time_ms": 312
    }
  ]
}
```

**Error Responses:**
- `404` - User not found

---

### 4. Get Assistant Status

Get the current status of the AI assistant.

**Endpoint:** `GET /api/assistant/status`

**cURL:**
```bash
curl -X GET http://localhost:5000/api/assistant/status
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Assistant status retrieved successfully",
  "data": {
    "name": "Minix",
    "initialized": true,
    "provider": "cohere"
  }
}
```

---

### 5. Reset Assistant

Reset the AI assistant's state and conversation context.

**Endpoint:** `POST /api/assistant/reset`

**cURL:**
```bash
curl -X POST http://localhost:5000/api/assistant/reset \
  -H "Content-Type: application/json"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Assistant reset successfully",
  "data": {
    "name": "Minix",
    "initialized": true
  }
}
```

**Error Responses:**
- `500` - Server error

---

## Statistics Endpoints

### Get System Statistics

Retrieve comprehensive system statistics.

**Endpoint:** `GET /stats`

**cURL:**
```bash
curl -X GET http://localhost:5000/stats
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Statistics retrieved successfully",
  "data": {
    "total_users": 42,
    "total_questions": 156,
    "average_response_time_ms": 234.5,
    "average_confidence_score": 0.82,
    "assistant_status": {
      "name": "Minix",
      "initialized": true,
      "provider": "cohere"
    }
  }
}
```

**Error Responses:**
- `500` - Server error

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "status": "error",
  "message": "Validation error",
  "error": "Missing required field: username"
}
```

#### 404 Not Found
```json
{
  "status": "error",
  "message": "User not found",
  "error": "No user found with the given ID"
}
```

#### 409 Conflict
```json
{
  "status": "error",
  "message": "Conflict",
  "error": "Username already exists"
}
```

#### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Server error",
  "error": "Database connection failed"
}
```

---

## Testing Tools

### 1. Swagger UI (Recommended)

Visit the interactive documentation:
```
http://localhost:5000/apidocs
```

Features:
- View all endpoints
- Test API calls in browser
- See request/response schemas
- No additional tools needed

---

### 2. cURL

All examples above use cURL. Basic syntax:

```bash
# GET request
curl -X GET http://localhost:5000/endpoint

# POST request
curl -X POST http://localhost:5000/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# PUT request
curl -X PUT http://localhost:5000/endpoint/id \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# DELETE request
curl -X DELETE http://localhost:5000/endpoint/id
```

---

### 3. Python Script

```python
import requests

BASE_URL = "http://localhost:5000"

# Create user
response = requests.post(
    f"{BASE_URL}/users",
    json={"username": "testuser", "email": "test@example.com"}
)
user_id = response.json()['data']['user']['id']

# Ask question
response = requests.post(
    f"{BASE_URL}/api/ask",
    json={"question": "What is AI?", "user_id": user_id}
)
print(response.json())

# Get conversation
response = requests.get(f"{BASE_URL}/api/conversation/{user_id}")
print(response.json())
```

---

### 4. Postman

Import the OpenAPI specification:
1. Download from: `http://localhost:5000/apispec_1.json`
2. Import into Postman
3. All endpoints will be available for testing

---

### 5. JavaScript/Fetch

```javascript
// Create user
fetch('http://localhost:5000/users', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        username: 'testuser',
        email: 'test@example.com'
    })
})
.then(res => res.json())
.then(data => {
    const userId = data.data.user.id;
    
    // Ask question
    return fetch('http://localhost:5000/api/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            question: 'What is AI?',
            user_id: userId
        })
    });
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Complete Workflow Example

### Scenario: Create user, ask questions, view history

```bash
#!/bin/bash

BASE_URL="http://localhost:5000"

# Step 1: Create a user
echo "Creating user..."
USER_RESPONSE=$(curl -s -X POST $BASE_URL/users \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com"}')

# Extract user ID (using jq)
USER_ID=$(echo $USER_RESPONSE | jq -r '.data.user.id')
echo "Created user with ID: $USER_ID"

# Step 2: Ask multiple questions
echo -e "\nAsking questions..."

curl -X POST $BASE_URL/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What time is it?\", \"user_id\": \"$USER_ID\"}"

curl -X POST $BASE_URL/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"Tell me about AI\", \"user_id\": \"$USER_ID\"}"

curl -X POST $BASE_URL/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is machine learning?\", \"user_id\": \"$USER_ID\"}"

# Step 3: Get conversation history
echo -e "\nFetching conversation history..."
curl -X GET "$BASE_URL/api/conversation/$USER_ID"

# Step 4: Get system stats
echo -e "\nFetching system statistics..."
curl -X GET $BASE_URL/stats

# Step 5: Get user details
echo -e "\nFetching user details..."
curl -X GET "$BASE_URL/users/$USER_ID"
```

---

## Quick Reference

### Endpoint Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| **Health & System** |
| GET | `/health` | Health check |
| GET | `/ping` | Ping test |
| GET | `/stats` | System statistics |
| **Users** |
| POST | `/users` | Create user |
| GET | `/users` | Get all users |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |
| GET | `/users/{id}/questions` | Get user's questions |
| **Questions** |
| POST | `/questions` | Create question record |
| GET | `/questions` | Get all questions |
| GET | `/questions/{id}` | Get question by ID |
| DELETE | `/questions/{id}` | Delete question |
| **AI Assistant** |
| GET | `/api/example-questions` | Get examples |
| POST | `/api/ask` | Ask question |
| GET | `/api/conversation/{id}` | Get conversation |
| GET | `/api/assistant/status` | Get status |
| POST | `/api/assistant/reset` | Reset assistant |

---

## Additional Resources

- **Swagger UI**: http://localhost:5000/apidocs
- **OpenAPI Spec**: http://localhost:5000/apispec_1.json
- **Quick Start Guide**: [docs/SWAGGER_QUICKSTART.md](docs/SWAGGER_QUICKSTART.md)
- **Complete API Reference**: [docs/API_ENDPOINTS.md](docs/API_ENDPOINTS.md)
- **Models Analysis**: [docs/MODELS_ANALYSIS.md](docs/MODELS_ANALYSIS.md)

---

## Support

For issues or questions:
- Check the Swagger UI for interactive testing
- Review the error responses for troubleshooting
- Consult the additional documentation in the `docs/` folder

---

**Last Updated:** October 2, 2025  
**API Version:** 1.0.0  
**Server:** Flask Development Server
