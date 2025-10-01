# API Endpoints Documentation

This document provides a comprehensive list of all available API endpoints in the AI Voice Assistant project.

## Interactive Documentation

For interactive API documentation with the ability to test endpoints directly in your browser:
- **Swagger UI**: http://localhost:5000/apidocs
- **OpenAPI Spec**: http://localhost:5000/apispec_1.json

---

## Health & System

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the server is running and healthy
- **Tags**: Health
- **Response**: Server status and timestamp

### Ping
- **Endpoint**: `GET /ping`
- **Description**: Simple ping endpoint to verify server connectivity
- **Tags**: Health
- **Response**: Pong HTML response

### System Statistics
- **Endpoint**: `GET /stats`
- **Description**: Get comprehensive system statistics including user counts, question counts, and AI assistant status
- **Tags**: Statistics
- **Response**: System statistics object with assistant status

---

## Web Interface

### Home Page
- **Endpoint**: `GET /`
- **Description**: Returns the main web interface HTML page
- **Tags**: Web Interface
- **Response**: HTML page

---

## User Management

### Create User
- **Endpoint**: `POST /users`
- **Description**: Create a new user in the system
- **Tags**: Users
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com"
  }
  ```
- **Response**: Created user object with ID and timestamps

### Get All Users
- **Endpoint**: `GET /users`
- **Description**: Retrieve a list of all registered users
- **Tags**: Users
- **Response**: Array of user objects

### Get User by ID
- **Endpoint**: `GET /users/<user_id>`
- **Description**: Get details of a specific user
- **Tags**: Users
- **Path Parameters**:
  - `user_id` (string, required): The unique identifier of the user
- **Response**: User object
- **Error Responses**: 404 if user not found

### Update User
- **Endpoint**: `PUT /users/<user_id>`
- **Description**: Update an existing user's information
- **Tags**: Users
- **Path Parameters**:
  - `user_id` (string, required): The unique identifier of the user
- **Request Body**:
  ```json
  {
    "name": "Jane Doe",
    "email": "jane.doe@example.com"
  }
  ```
- **Response**: Updated user object
- **Error Responses**: 404 if user not found, 400 for validation errors

### Delete User
- **Endpoint**: `DELETE /users/<user_id>`
- **Description**: Delete a user from the system
- **Tags**: Users
- **Path Parameters**:
  - `user_id` (string, required): The unique identifier of the user
- **Response**: Success message
- **Error Responses**: 404 if user not found

### Get User's Questions
- **Endpoint**: `GET /users/<user_id>/questions`
- **Description**: Get all questions asked by a specific user
- **Tags**: Users
- **Path Parameters**:
  - `user_id` (string, required): The unique identifier of the user
- **Response**: Array of question-response objects for the user
- **Error Responses**: 404 if user not found

---

## Question Management

### Create Question-Response Record
- **Endpoint**: `POST /questions`
- **Description**: Create a new question-response record
- **Tags**: Questions
- **Request Body**:
  ```json
  {
    "user_id": "user123",
    "question": "What is artificial intelligence?",
    "response": "Artificial intelligence is...",
    "confidence_score": 0.85,
    "response_time_ms": 250
  }
  ```
- **Response**: Created question-response record
- **Error Responses**: 400 for validation errors

### Get All Question-Responses
- **Endpoint**: `GET /questions`
- **Description**: Retrieve all question-response records
- **Tags**: Questions
- **Query Parameters**:
  - `limit` (integer, optional, default: 100): Maximum number of records to return
  - `offset` (integer, optional, default: 0): Number of records to skip for pagination
- **Response**: Array of question-response objects

### Get Question-Response by ID
- **Endpoint**: `GET /questions/<response_id>`
- **Description**: Get a specific question-response record
- **Tags**: Questions
- **Path Parameters**:
  - `response_id` (integer, required): The unique identifier of the question-response record
- **Response**: Question-response object
- **Error Responses**: 404 if record not found

### Delete Question-Response
- **Endpoint**: `DELETE /questions/<response_id>`
- **Description**: Delete a question-response record
- **Tags**: Questions
- **Path Parameters**:
  - `response_id` (integer, required): The unique identifier of the question-response record
- **Response**: Success message
- **Error Responses**: 404 if record not found

---

## AI Assistant API

### Get Example Questions
- **Endpoint**: `GET /api/example-questions`
- **Description**: Get a list of pre-configured example questions for the assistant
- **Tags**: API
- **Response**: Array of example questions with categories and descriptions

### Ask Assistant
- **Endpoint**: `POST /api/ask`
- **Description**: Ask a question to the AI assistant and get a response
- **Tags**: API
- **Request Body**:
  ```json
  {
    "question": "What time is it?",
    "user_id": "user123"  // optional
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "message": "Question processed successfully",
    "data": {
      "question": "What time is it?",
      "response": "The current time is 2:30 PM",
      "confidence_score": 0.95,
      "response_time_ms": 234,
      "timestamp": "2025-10-01T14:30:00Z",
      "user_id": "user123"
    }
  }
  ```
- **Error Responses**: 400 for validation errors

### Get User Conversation History
- **Endpoint**: `GET /api/conversation/<user_id>`
- **Description**: Get the conversation history for a specific user
- **Tags**: API
- **Path Parameters**:
  - `user_id` (string, required): The user ID
- **Query Parameters**:
  - `limit` (integer, optional, default: 50): Maximum number of conversations to return
  - `offset` (integer, optional, default: 0): Number of conversations to skip
- **Response**: Array of conversation objects ordered by timestamp
- **Error Responses**: 404 if user not found

### Get Assistant Status
- **Endpoint**: `GET /api/assistant/status`
- **Description**: Get the current status of the AI assistant
- **Tags**: API
- **Response**:
  ```json
  {
    "status": "success",
    "message": "...",
    "data": {
      "name": "Minix",
      "initialized": true,
      "provider": "cohere"
    }
  }
  ```

### Reset Assistant
- **Endpoint**: `POST /api/assistant/reset`
- **Description**: Reset the AI assistant's state and conversation context
- **Tags**: API
- **Response**: Success message with assistant status
- **Error Responses**: 500 for server errors

---

## Response Format

All API endpoints follow a consistent response format:

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

---

## HTTP Status Codes

- **200 OK**: Successful GET, PUT, DELETE operations
- **201 Created**: Successful POST operations that create a resource
- **400 Bad Request**: Validation errors or malformed requests
- **404 Not Found**: Requested resource doesn't exist
- **500 Internal Server Error**: Server-side errors

---

## Authentication

Currently, the API does not require authentication. This should be added for production use.

---

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for:
- `http://localhost:*`
- `http://127.0.0.1:*`

---

## Rate Limiting

Currently, there is no rate limiting implemented. Consider adding rate limiting for production deployment.

---

## Testing the API

You can test the API using:

1. **Swagger UI**: http://localhost:5000/apidocs (Interactive documentation)
2. **curl**: Command-line tool
   ```bash
   curl -X POST http://localhost:5000/api/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What time is it?"}'
   ```
3. **Postman**: Import the OpenAPI specification from http://localhost:5000/apispec_1.json
4. **Python requests**:
   ```python
   import requests
   
   response = requests.post(
       'http://localhost:5000/api/ask',
       json={'question': 'What time is it?'}
   )
   print(response.json())
   ```

---

## Additional Resources

- [API Integration Guide](./API_GUIDE.md)
- [Flutter Integration Guide](./FLUTTER_INTEGRATION_GUIDE.md)
- [Project README](../README.md)

---

Last Updated: October 1, 2025
