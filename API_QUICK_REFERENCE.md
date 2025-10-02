# API Quick Reference Card

## Base URL
```
http://localhost:5000
```

## Essential Endpoints & cURL Commands

### 🏥 Health Check
```bash
curl http://localhost:5000/health
```

### 👤 Create User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "myuser", "email": "user@example.com"}'
```

### 🤖 Ask AI Assistant
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What time is it?", "user_id": "USER_ID_HERE"}'
```

### 💬 Get Conversation History
```bash
curl http://localhost:5000/api/conversation/USER_ID_HERE
```

### 📊 Get Statistics
```bash
curl http://localhost:5000/stats
```

### 👥 Get All Users
```bash
curl http://localhost:5000/users
```

### ❓ Get Example Questions
```bash
curl http://localhost:5000/api/example-questions
```

### 🔧 Update User
```bash
curl -X PUT http://localhost:5000/users/USER_ID_HERE \
  -H "Content-Type: application/json" \
  -d '{"username": "newusername", "email": "newemail@example.com"}'
```

### 🗑️ Delete User
```bash
curl -X DELETE http://localhost:5000/users/USER_ID_HERE
```

### 🔄 Reset Assistant
```bash
curl -X POST http://localhost:5000/api/assistant/reset
```

---

## Complete Workflow

```bash
# 1. Create user
USER_ID=$(curl -s -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com"}' \
  | jq -r '.data.user.id')

# 2. Ask question
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is AI?\",\"user_id\":\"$USER_ID\"}"

# 3. View conversation
curl http://localhost:5000/api/conversation/$USER_ID
```

---

## Interactive Testing
**Swagger UI:** http://localhost:5000/apidocs

---

## Response Format
```json
{
  "status": "success|error",
  "message": "Description",
  "data": { /* Response data */ }
}
```

---

## Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `409` - Conflict
- `500` - Server Error

---

For complete documentation, see: [API_GUIDE.md](API_GUIDE.md)
