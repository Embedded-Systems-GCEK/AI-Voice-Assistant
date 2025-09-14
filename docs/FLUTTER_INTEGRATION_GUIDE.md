# AI Voice Assistant - Flutter Integration Guide

## Overview
This guide shows how to integrate the AI Voice Assistant with the Flutter app, including example questions and real-time API communication.

## Features Implemented

### 1. Backend API Endpoints
- `/api/example-questions` - Get categorized example questions
- `/api/ask` - Ask questions to the AI assistant
- `/api/conversation/<user_id>` - Get user conversation history
- `/api/assistant/status` - Get assistant status
- `/api/assistant/reset` - Reset assistant conversation

### 2. Flutter Integration
- **ApiService** - HTTP client for backend communication
- **AiChatScreen** - Interactive chat interface
- **Example Questions** - Categorized question suggestions
- **Real-time Chat** - Messaging interface with the assistant

## Usage Instructions

### 1. Start the Backend Server
```bash
cd e:\Git\ES-GCEK\AI-Voice-Assistant\src\ui
python server.py
```

The server will start on `http://localhost:5000`

### 2. Run the Flutter App
```bash
cd e:\Git\ES-GCEK\AI-Voice-Assistant-UI\ai_voice_assistant
flutter run -d chrome  # For web
# or
flutter run -d windows  # For desktop (after installing Visual Studio)
```

### 3. Using the AI Chat Interface

#### Example Questions
- Questions are categorized (General, Personal, Knowledge, etc.)
- Click on any example question to ask it automatically
- Filter questions by category using the dropdown

#### Chat Interface
- Type messages in the input field
- Press Enter or click the send button
- View conversation history with timestamps
- See typing indicators when assistant is responding

## API Testing with cURL

### 1. Get Example Questions
```bash
curl -X GET "http://localhost:5000/api/example-questions" \
  -H "Content-Type: application/json"
```

### 2. Ask a Question
```bash
curl -X POST "http://localhost:5000/api/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What time is it?",
    "user_id": "optional-user-id"
  }'
```

### 3. Get Assistant Status
```bash
curl -X GET "http://localhost:5000/api/assistant/status" \
  -H "Content-Type: application/json"
```

### 4. Create a User (for conversation tracking)
```bash
curl -X POST "http://localhost:5000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com"
  }'
```

### 5. Get User Conversation History
```bash
curl -X GET "http://localhost:5000/api/conversation/USER_ID" \
  -H "Content-Type: application/json"
```

## Example Questions Available

### General
- "What time is it?"
- "What's the date today?"
- "What day is it?"

### Personal
- "How are you?"
- "What's your name?"

### Knowledge
- "Tell me about artificial intelligence"
- "What is machine learning?"
- "Explain quantum computing"

### Weather
- "What's the weather like?"

### Technology & Help
- "What can you help me with?"

## Flutter App Navigation

The AI Chat feature is integrated into the main app navigation:
1. **Dashboard** - Main overview
2. **Conversations** - Existing conversation screen
3. **AI Chat** - New AI assistant chat interface ⭐
4. **Map** - Location features
5. **Users** - User management

## Features Demonstration

### 1. Example Questions UI
- Horizontal scrollable list of question cards
- Category filtering
- One-click question asking
- Visual category tags

### 2. Chat Interface
- Real-time messaging
- User/Assistant message differentiation
- Timestamp display
- Auto-scroll to latest messages
- Loading indicators

### 3. Error Handling
- Network connection errors
- Server unavailability
- API response errors
- User-friendly error messages

## Backend Integration Details

### Assistant Integration
The backend now includes:
- Direct integration with the Python assistant modules
- Fallback responses when assistant is unavailable
- Response time tracking
- Confidence scoring
- Conversation state management

### Database Storage
- User management with SQLAlchemy ORM
- Question/response history
- Conversation tracking
- Statistics and analytics

## Testing the Integration

### 1. Test Backend Only
```bash
# In the backend directory
python demo_timeout.py
```

### 2. Test API Endpoints
Use the provided cURL commands or a tool like Postman

### 3. Test Flutter App
Run the Flutter app and navigate to the "AI Chat" tab

### 4. End-to-End Test
1. Start the backend server
2. Run the Flutter app
3. Create a user (optional)
4. Ask questions using example questions or custom input
5. View conversation history

## Troubleshooting

### Common Issues
1. **Server not starting**: Check Python dependencies
2. **Flutter build errors**: Run `flutter clean && flutter pub get`
3. **Connection refused**: Ensure backend is running on localhost:5000
4. **Assistant not responding**: Check backend logs for assistant initialization

### Dependencies Required
- Flask, Flask-SQLAlchemy for backend
- speech_recognition, other assistant dependencies
- Flutter http package for API calls

## Next Steps

### Potential Enhancements
1. **Voice Integration**: Add speech-to-text in Flutter
2. **User Authentication**: Add login/signup flow
3. **Real-time Updates**: WebSocket integration
4. **Offline Mode**: Local assistant responses
5. **Push Notifications**: For important assistant responses
6. **Analytics Dashboard**: Usage statistics and insights

This integration provides a solid foundation for AI-powered conversations within your Flutter application!
