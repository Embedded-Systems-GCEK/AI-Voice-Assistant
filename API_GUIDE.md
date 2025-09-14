# AI Voice Assistant - API Integration Guide

## Overview

This guide explains how to run the AI Voice Assistant with full API support for Flutter integration. The system provides multiple endpoints to get current questions, answers, conversation statistics, and real-time assistant status.

## 🚀 Quick Start

### Option 1: Use PowerShell Script (Recommended)
```powershell
cd src
.\start_servers.ps1
```

### Option 2: Use Batch File
```cmd
cd src
start_servers.bat
```

### Option 3: Use Python Launcher
```bash
cd src
python launcher.py
```

### Option 4: Manual Start (Individual Servers)
```bash
# Terminal 1 - API Server (Primary for Flutter)
cd src
python api_server.py

# Terminal 2 - Unified Server (Web UI + Database & Core APIs)
cd src  
python server/server.py
```

## 📊 Server Architecture

| Server | Port | Purpose | Primary Use |
|--------|------|---------|-------------|
| **API Server** | 5001 | Real-time assistant API | **Flutter App** |
| **Unified Server** | 5000 | Web UI + Database + Core APIs | Web Browser & Data |

## 🔗 API Endpoints for Flutter

### Base URL: `http://localhost:5001`

### 1. **GET /api/status**
Get current assistant status and conversation info
```json
{
  "status": "success",
  "data": {
    "assistant_status": "ready",
    "current_question": "What time is it?",
    "current_answer": "The current time is 2:30 PM",
    "question_count": 5,
    "session_id": "uuid-here",
    "conversation_length": 5
  }
}
```

### 2. **POST /api/ask**
Send a question to the assistant
```json
// Request
{
  "question": "What time is it?",
  "user_id": "optional-user-id"
}

// Response
{
  "status": "success", 
  "data": {
    "question": "What time is it?",
    "answer": "The current time is 2:30 PM",
    "question_number": 1,
    "session_id": "uuid-here"
  }
}
```

### 3. **GET /api/conversation**
Get conversation history
```json
{
  "status": "success",
  "data": {
    "conversation": [
      {
        "id": 1,
        "question": "What time is it?", 
        "answer": "2:30 PM",
        "timestamp": "2025-09-12T14:30:00Z",
        "user_id": "anonymous"
      }
    ],
    "total_count": 1
  }
}
```

### 4. **GET /api/stats**
Get conversation statistics
```json
{
  "status": "success",
  "data": {
    "total_questions": 5,
    "conversation_entries": 5,
    "session_id": "uuid-here",
    "assistant_status": "ready"
  }
}
```

### 5. **GET /api/example-questions**
Get predefined example questions
```json
{
  "status": "success", 
  "data": {
    "questions": [
      {
        "id": 1,
        "category": "General",
        "question": "What time is it?",
        "description": "Ask for current time"
      }
    ],
    "categories": ["General", "Personal", "Knowledge"]
  }
}
```

### 6. **POST /api/reset**
Reset conversation and assistant state
```json
{
  "status": "success",
  "message": "Conversation reset successfully",
  "data": {
    "session_id": "new-uuid-here"
  }
}
```

## 📱 Flutter Integration Example

### 1. HTTP Service Class
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class AssistantApiService {
  static const String baseUrl = 'http://localhost:5001';
  
  // Get current status
  static Future<Map<String, dynamic>> getStatus() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/status'),
      headers: {'Content-Type': 'application/json'},
    );
    return json.decode(response.body);
  }
  
  // Ask a question
  static Future<Map<String, dynamic>> askQuestion(String question, {String? userId}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/ask'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'question': question,
        if (userId != null) 'user_id': userId,
      }),
    );
    return json.decode(response.body);
  }
  
  // Get conversation history
  static Future<List<dynamic>> getConversation({String? userId, int? limit}) async {
    var uri = Uri.parse('$baseUrl/api/conversation');
    if (userId != null || limit != null) {
      uri = uri.replace(queryParameters: {
        if (userId != null) 'user_id': userId,
        if (limit != null) 'limit': limit.toString(),
      });
    }
    
    final response = await http.get(uri);
    final data = json.decode(response.body);
    return data['data']['conversation'];
  }
  
  // Get example questions
  static Future<List<dynamic>> getExampleQuestions({String? category}) async {
    var uri = Uri.parse('$baseUrl/api/example-questions');
    if (category != null) {
      uri = uri.replace(queryParameters: {'category': category});
    }
    
    final response = await http.get(uri);
    final data = json.decode(response.body);
    return data['data']['questions'];
  }
  
  // Reset conversation
  static Future<Map<String, dynamic>> resetConversation() async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/reset'),
      headers: {'Content-Type': 'application/json'},
    );
    return json.decode(response.body);
  }
}
```

### 2. Real-time Status Updates
```dart
class AssistantStatusProvider extends ChangeNotifier {
  Timer? _statusTimer;
  
  String assistantStatus = 'idle';
  String currentQuestion = '';
  String currentAnswer = '';
  int questionCount = 0;
  
  void startStatusPolling() {
    _statusTimer = Timer.periodic(Duration(seconds: 2), (timer) async {
      try {
        final status = await AssistantApiService.getStatus();
        if (status['status'] == 'success') {
          assistantStatus = status['data']['assistant_status'];
          currentQuestion = status['data']['current_question'];
          currentAnswer = status['data']['current_answer']; 
          questionCount = status['data']['question_count'];
          notifyListeners();
        }
      } catch (e) {
        print('Status polling error: $e');
      }
    });
  }
  
  void stopStatusPolling() {
    _statusTimer?.cancel();
  }
}
```

### 3. Chat Interface Example
```dart
class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  List<Map<String, dynamic>> messages = [];
  bool isLoading = false;
  
  @override
  void initState() {
    super.initState();
    _loadConversationHistory();
  }
  
  Future<void> _loadConversationHistory() async {
    try {
      final conversation = await AssistantApiService.getConversation();
      setState(() {
        messages = List<Map<String, dynamic>>.from(conversation);
      });
    } catch (e) {
      print('Error loading conversation: $e');
    }
  }
  
  Future<void> _sendMessage(String message) async {
    if (message.trim().isEmpty) return;
    
    setState(() {
      isLoading = true;
    });
    
    try {
      final response = await AssistantApiService.askQuestion(message);
      if (response['status'] == 'success') {
        setState(() {
          messages.add({
            'question': message,
            'answer': response['data']['answer'],
            'timestamp': DateTime.now().toIso8601String(),
          });
        });
        _messageController.clear();
      }
    } catch (e) {
      // Handle error
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('AI Assistant Chat')),
      body: Column(
        children: [
          // Messages list
          Expanded(
            child: ListView.builder(
              itemCount: messages.length,
              itemBuilder: (context, index) {
                final msg = messages[index];
                return ChatBubble(
                  question: msg['question'],
                  answer: msg['answer'],
                  timestamp: msg['timestamp'],
                );
              },
            ),
          ),
          
          // Loading indicator
          if (isLoading)
            LinearProgressIndicator(),
          
          // Input field
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'Ask a question...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: _sendMessage,
                  ),
                ),
                IconButton(
                  onPressed: () => _sendMessage(_messageController.text),
                  icon: Icon(Icons.send),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

## 🧪 Testing the APIs

### Test all endpoints:
```bash
cd src
python launcher.py --test
```

### Manual testing with curl:
```bash
# Get status
curl http://localhost:5001/api/status

# Ask question
curl -X POST http://localhost:5001/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What time is it?"}'

# Get conversation
curl http://localhost:5001/api/conversation

# Get example questions  
curl http://localhost:5001/api/example-questions
```

## 🔧 Configuration

### Ports
- API Server: 5001 (Primary for Flutter)
- Main Server: 5000 (Database)
- UI Server: 5002 (Web UI)

### CORS
All servers are configured with CORS enabled for cross-origin requests.

### Error Handling
All endpoints return standardized JSON responses with status and error information.

## 📚 Additional Resources

- **Flutter Integration Guide**: `docs/FLUTTER_INTEGRATION_GUIDE.md`
- **Timeout Guide**: `docs/TIMEOUT_GUIDE.md` 
- **Server Architecture**: Unified `src/server/` (includes web UI functionality)

---

**Need Help?** 
- Run `python launcher.py --guide` for detailed Flutter integration examples
- Check the server logs for debugging information
- Use the `/health` endpoint to verify server status