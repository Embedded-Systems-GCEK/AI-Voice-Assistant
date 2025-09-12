📱 FLUTTER INTEGRATION GUIDE
═══════════════════════════════════════════════════════════════

1. 🔧 SETUP YOUR FLUTTER HTTP CLIENT:

```dart
class ApiService {
  static const String baseUrl = 'http://localhost:5001';
  
  static Future<Map<String, dynamic>> getStatus() async {
    final response = await http.get(Uri.parse('$baseUrl/api/status'));
    return json.decode(response.body);
  }
  
  static Future<Map<String, dynamic>> askQuestion(String question) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/ask'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'question': question}),
    );
    return json.decode(response.body);
  }
  
  static Future<Map<String, dynamic>> getConversation() async {
    final response = await http.get(Uri.parse('$baseUrl/api/conversation'));
    return json.decode(response.body);
  }
  
  static Future<List<dynamic>> getExampleQuestions() async {
    final response = await http.get(Uri.parse('$baseUrl/api/example-questions'));
    final data = json.decode(response.body);
    return data['data']['questions'];
  }
}
```

2. 📊 REAL-TIME STATUS MONITORING:

```dart
Timer.periodic(Duration(seconds: 2), (timer) async {
  final status = await ApiService.getStatus();
  setState(() {
    currentQuestion = status['data']['current_question'];
    currentAnswer = status['data']['current_answer'];
    questionCount = status['data']['question_count'];
    assistantStatus = status['data']['assistant_status'];
  });
});
```

3. 🗨️ EXAMPLE CHAT IMPLEMENTATION:

```dart
Future<void> sendMessage(String message) async {
  setState(() {
    isLoading = true;
  });
  
  try {
    final response = await ApiService.askQuestion(message);
    if (response['status'] == 'success') {
      setState(() {
        // Add to chat history
        chatMessages.add({
          'question': message,
          'answer': response['data']['answer'],
          'timestamp': DateTime.now(),
        });
      });
    }
  } catch (e) {
    // Handle error
  } finally {
    setState(() {
      isLoading = false;
    });
  }
}
```

4. 🎯 KEY API ENDPOINTS FOR YOUR FLUTTER APP:

   • GET  /api/status           → Current assistant status, Q&A, counters
   • POST /api/ask              → Send questions, get responses  
   • GET  /api/conversation     → Full conversation history
   • GET  /api/stats            → Usage statistics
   • GET  /api/example-questions → Predefined questions
   • POST /api/reset            → Reset conversation state

5. 📱 RECOMMENDED FLUTTER FEATURES:

   • Real-time status updates (Timer or WebSocket)
   • Chat interface with message history
   • Example questions as quick buttons
   • Loading states and error handling
   • Conversation statistics display
   • Reset conversation functionality

═══════════════════════════════════════════════════════════════
    