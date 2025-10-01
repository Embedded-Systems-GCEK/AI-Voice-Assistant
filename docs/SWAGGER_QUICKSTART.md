# Swagger UI Quick Start Guide

## Accessing the Documentation

Once your server is running, navigate to:
```
http://localhost:5000/apidocs
```

## What You'll See

The Swagger UI provides an interactive interface with the following sections:

### Header Section
- **API Title**: AI Voice Assistant API
- **Version**: 1.0.0
- **Description**: REST API for AI Voice Assistant with user management and conversation features
- **Contact**: Link to Embedded Systems GCEK GitHub

### Endpoint Categories (Tags)

#### 🏥 Health
Endpoints for checking server health and connectivity
- GET /health
- GET /ping

#### 🌐 Web Interface
HTML page endpoints
- GET /

#### 👥 Users
Complete user management CRUD operations
- POST /users
- GET /users
- GET /users/{user_id}
- PUT /users/{user_id}
- DELETE /users/{user_id}
- GET /users/{user_id}/questions

#### ❓ Questions
Question-response record management
- POST /questions
- GET /questions
- GET /questions/{response_id}
- DELETE /questions/{response_id}

#### 🤖 API
AI assistant interaction endpoints
- GET /api/example-questions
- POST /api/ask
- GET /api/conversation/{user_id}
- GET /api/assistant/status
- POST /api/assistant/reset

#### 📊 Statistics
System metrics and statistics
- GET /stats

## Using the Interactive Features

### 1. Viewing Endpoint Details
Click on any endpoint to expand it and see:
- Description
- Parameters (path, query, body)
- Request body schema
- Response examples
- Possible status codes

### 2. Testing Endpoints

#### GET Requests
1. Click on the endpoint (e.g., GET /users)
2. Click "Try it out" button
3. Fill in any required parameters
4. Click "Execute"
5. View the response below

#### POST/PUT Requests
1. Click on the endpoint (e.g., POST /api/ask)
2. Click "Try it out"
3. Edit the JSON request body in the text area
4. Click "Execute"
5. View the response

### 3. Example: Testing the Ask Assistant Endpoint

**Step 1**: Navigate to POST /api/ask

**Step 2**: Click "Try it out"

**Step 3**: Modify the request body:
```json
{
  "question": "What is the weather like today?",
  "user_id": "test-user-123"
}
```

**Step 4**: Click "Execute"

**Step 5**: View Response:
```json
{
  "status": "success",
  "message": "Question processed successfully",
  "data": {
    "question": "What is the weather like today?",
    "response": "I don't have real-time access to weather data...",
    "confidence_score": 0.8,
    "response_time_ms": 234,
    "timestamp": "2025-10-01T14:30:00Z",
    "user_id": "test-user-123"
  }
}
```

## Understanding Request Schemas

### Required Fields
Fields marked with a red asterisk (*) are required.

### Optional Fields
Fields without an asterisk are optional.

### Data Types
Each field shows its expected data type:
- `string` - Text data
- `integer` - Whole numbers
- `number` - Decimal numbers
- `boolean` - true/false
- `object` - Nested JSON object
- `array` - List of items

## Understanding Response Codes

### Success Codes
- **200 OK**: Successful request (GET, PUT, DELETE)
- **201 Created**: Successfully created resource (POST)

### Error Codes
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server error

## Tips for Using Swagger UI

### 1. Search Functionality
Use your browser's search (Ctrl+F / Cmd+F) to quickly find specific endpoints.

### 2. Collapsing Sections
Click the tag name to collapse/expand entire sections of endpoints.

### 3. Model Schemas
Scroll to the bottom to see reusable data model definitions.

### 4. Download OpenAPI Spec
The raw OpenAPI specification is available at:
```
http://localhost:5000/apispec_1.json
```

### 5. Integration with Tools
You can import the OpenAPI spec into:
- Postman
- Insomnia
- API testing frameworks
- Code generators

## Common Use Cases

### Creating a New User
1. Expand POST /users
2. Try it out
3. Modify request body:
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```
4. Execute and save the returned user_id

### Asking a Question
1. Expand POST /api/ask
2. Try it out
3. Enter your question:
```json
{
  "question": "Tell me about AI",
  "user_id": "the-id-from-previous-step"
}
```
4. Execute to get the assistant's response

### Viewing Conversation History
1. Expand GET /api/conversation/{user_id}
2. Try it out
3. Enter the user_id
4. Optionally set limit and offset
5. Execute to see the conversation history

### Getting System Statistics
1. Expand GET /stats
2. Try it out
3. Execute to see:
   - Total users
   - Total questions
   - Average response time
   - Assistant status

## Troubleshooting

### Can't Access Swagger UI
- Ensure server is running: `python src/app.py`
- Check the correct URL: http://localhost:5000/apidocs
- Verify no firewall blocking port 5000

### "Try it out" Not Working
- Check request body JSON syntax
- Ensure required fields are filled
- Look at error messages in response

### CORS Errors
- Ensure your client origin is in the allowed CORS origins
- Check browser console for specific CORS errors

## Integration Examples

### Using curl
```bash
# Create user
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'

# Ask question
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What time is it?"}'
```

### Using Python
```python
import requests

# Create user
response = requests.post(
    'http://localhost:5000/users',
    json={'name': 'John Doe', 'email': 'john@example.com'}
)
user = response.json()

# Ask question
response = requests.post(
    'http://localhost:5000/api/ask',
    json={'question': 'What time is it?', 'user_id': user['data']['id']}
)
print(response.json())
```

### Using JavaScript/Fetch
```javascript
// Create user
const createUser = async () => {
  const response = await fetch('http://localhost:5000/users', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name: 'John Doe', email: 'john@example.com'})
  });
  return await response.json();
};

// Ask question
const askQuestion = async (userId) => {
  const response = await fetch('http://localhost:5000/api/ask', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question: 'What time is it?', user_id: userId})
  });
  return await response.json();
};
```

---

## Need More Help?

- Check the comprehensive API documentation: `docs/API_ENDPOINTS.md`
- Review the API guide: `API_GUIDE.md`
- See Flutter integration: `docs/FLUTTER_INTEGRATION_GUIDE.md`

---

Happy Testing! 🚀
