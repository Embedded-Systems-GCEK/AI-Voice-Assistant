// AI Voice Assistant - Flutter/Dart API Integration Template
// Complete implementation example for Flutter apps

import 'dart:convert';
import 'dart:async';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';

// =============================================================================
// API SERVICE CLASS
// =============================================================================
class AssistantApiService {
  static const String baseUrl = 'http://localhost:5001';
  static const Duration timeoutDuration = Duration(seconds: 30);
  
  // Headers for all requests
  static Map<String, String> get headers => {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };
  
  // Error handling helper
  static Map<String, dynamic> _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return json.decode(response.body);
    } else {
      throw Exception('API Error ${response.statusCode}: ${response.body}');
    }
  }
  
  // GET /api/status - Get current assistant status
  static Future<AssistantStatus> getStatus() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/status'),
        headers: headers,
      ).timeout(timeoutDuration);
      
      final data = _handleResponse(response);
      return AssistantStatus.fromJson(data['data']);
    } catch (e) {
      throw Exception('Failed to get status: $e');
    }
  }
  
  // POST /api/ask - Ask a question
  static Future<QuestionResponse> askQuestion(String question, {String? userId}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/ask'),
        headers: headers,
        body: json.encode({
          'question': question,
          if (userId != null) 'user_id': userId,
        }),
      ).timeout(timeoutDuration);
      
      final data = _handleResponse(response);
      return QuestionResponse.fromJson(data['data']);
    } catch (e) {
      throw Exception('Failed to ask question: $e');
    }
  }
  
  // GET /api/conversation - Get conversation history
  static Future<List<ConversationEntry>> getConversation({
    String? userId, 
    int? limit
  }) async {
    try {
      var uri = Uri.parse('$baseUrl/api/conversation');
      
      // Add query parameters
      final queryParams = <String, String>{};
      if (userId != null) queryParams['user_id'] = userId;
      if (limit != null) queryParams['limit'] = limit.toString();
      
      if (queryParams.isNotEmpty) {
        uri = uri.replace(queryParameters: queryParams);
      }
      
      final response = await http.get(uri, headers: headers).timeout(timeoutDuration);
      final data = _handleResponse(response);
      
      final conversationList = data['data']['conversation'] as List;
      return conversationList
          .map((item) => ConversationEntry.fromJson(item))
          .toList();
    } catch (e) {
      throw Exception('Failed to get conversation: $e');
    }
  }
  
  // GET /api/stats - Get statistics
  static Future<AssistantStats> getStats() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/stats'),
        headers: headers,
      ).timeout(timeoutDuration);
      
      final data = _handleResponse(response);
      return AssistantStats.fromJson(data['data']);
    } catch (e) {
      throw Exception('Failed to get stats: $e');
    }
  }
  
  // GET /api/example-questions - Get example questions
  static Future<List<ExampleQuestion>> getExampleQuestions({String? category}) async {
    try {
      var uri = Uri.parse('$baseUrl/api/example-questions');
      
      if (category != null) {
        uri = uri.replace(queryParameters: {'category': category});
      }
      
      final response = await http.get(uri, headers: headers).timeout(timeoutDuration);
      final data = _handleResponse(response);
      
      final questionsList = data['data']['questions'] as List;
      return questionsList
          .map((item) => ExampleQuestion.fromJson(item))
          .toList();
    } catch (e) {
      throw Exception('Failed to get example questions: $e');
    }
  }
  
  // POST /api/reset - Reset conversation
  static Future<ResetResponse> resetConversation() async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/reset'),
        headers: headers,
      ).timeout(timeoutDuration);
      
      final data = _handleResponse(response);
      return ResetResponse.fromJson(data['data']);
    } catch (e) {
      throw Exception('Failed to reset conversation: $e');
    }
  }
  
  // GET /health - Health check
  static Future<bool> checkHealth() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/health'),
        headers: headers,
      ).timeout(Duration(seconds: 5));
      
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

// =============================================================================
// DATA MODELS
// =============================================================================

class AssistantStatus {
  final String status;
  final bool assistantAvailable;
  final String currentQuestion;
  final String currentAnswer;
  final int questionCount;
  final String sessionId;
  final int conversationLength;
  final DateTime timestamp;
  
  AssistantStatus({
    required this.status,
    required this.assistantAvailable,
    required this.currentQuestion,
    required this.currentAnswer,
    required this.questionCount,
    required this.sessionId,
    required this.conversationLength,
    required this.timestamp,
  });
  
  factory AssistantStatus.fromJson(Map<String, dynamic> json) {
    return AssistantStatus(
      status: json['assistant_status'] ?? 'unknown',
      assistantAvailable: json['assistant_available'] ?? false,
      currentQuestion: json['current_question'] ?? '',
      currentAnswer: json['current_answer'] ?? '',
      questionCount: json['question_count'] ?? 0,
      sessionId: json['session_id'] ?? '',
      conversationLength: json['conversation_length'] ?? 0,
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}

class QuestionResponse {
  final String question;
  final String answer;
  final int questionNumber;
  final DateTime timestamp;
  final String sessionId;
  
  QuestionResponse({
    required this.question,
    required this.answer,
    required this.questionNumber,
    required this.timestamp,
    required this.sessionId,
  });
  
  factory QuestionResponse.fromJson(Map<String, dynamic> json) {
    return QuestionResponse(
      question: json['question'] ?? '',
      answer: json['answer'] ?? '',
      questionNumber: json['question_number'] ?? 0,
      timestamp: DateTime.parse(json['timestamp']),
      sessionId: json['session_id'] ?? '',
    );
  }
}

class ConversationEntry {
  final int id;
  final String question;
  final String answer;
  final DateTime timestamp;
  final String userId;
  final String sessionId;
  
  ConversationEntry({
    required this.id,
    required this.question,
    required this.answer,
    required this.timestamp,
    required this.userId,
    required this.sessionId,
  });
  
  factory ConversationEntry.fromJson(Map<String, dynamic> json) {
    return ConversationEntry(
      id: json['id'] ?? 0,
      question: json['question'] ?? '',
      answer: json['answer'] ?? '',
      timestamp: DateTime.parse(json['timestamp']),
      userId: json['user_id'] ?? '',
      sessionId: json['session_id'] ?? '',
    );
  }
}

class AssistantStats {
  final int totalQuestions;
  final int conversationEntries;
  final String sessionId;
  final String assistantStatus;
  final DateTime uptime;
  
  AssistantStats({
    required this.totalQuestions,
    required this.conversationEntries,
    required this.sessionId,
    required this.assistantStatus,
    required this.uptime,
  });
  
  factory AssistantStats.fromJson(Map<String, dynamic> json) {
    return AssistantStats(
      totalQuestions: json['total_questions'] ?? 0,
      conversationEntries: json['conversation_entries'] ?? 0,
      sessionId: json['session_id'] ?? '',
      assistantStatus: json['assistant_status'] ?? 'unknown',
      uptime: DateTime.parse(json['uptime']),
    );
  }
}

class ExampleQuestion {
  final int id;
  final String category;
  final String question;
  final String description;
  
  ExampleQuestion({
    required this.id,
    required this.category,
    required this.question,
    required this.description,
  });
  
  factory ExampleQuestion.fromJson(Map<String, dynamic> json) {
    return ExampleQuestion(
      id: json['id'] ?? 0,
      category: json['category'] ?? '',
      question: json['question'] ?? '',
      description: json['description'] ?? '',
    );
  }
}

class ResetResponse {
  final String sessionId;
  final DateTime timestamp;
  
  ResetResponse({
    required this.sessionId,
    required this.timestamp,
  });
  
  factory ResetResponse.fromJson(Map<String, dynamic> json) {
    return ResetResponse(
      sessionId: json['session_id'] ?? '',
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}

// =============================================================================
// STATE MANAGEMENT (using Provider)
// =============================================================================

class AssistantProvider extends ChangeNotifier {
  Timer? _statusTimer;
  AssistantStatus? _status;
  List<ConversationEntry> _conversation = [];
  AssistantStats? _stats;
  bool _isLoading = false;
  String? _error;
  
  // Getters
  AssistantStatus? get status => _status;
  List<ConversationEntry> get conversation => _conversation;
  AssistantStats? get stats => _stats;
  bool get isLoading => _isLoading;
  String? get error => _error;
  
  // Start real-time status polling
  void startStatusPolling({Duration interval = const Duration(seconds: 2)}) {
    _statusTimer?.cancel();
    _statusTimer = Timer.periodic(interval, (timer) async {
      try {
        _status = await AssistantApiService.getStatus();
        _error = null;
        notifyListeners();
      } catch (e) {
        _error = e.toString();
        notifyListeners();
      }
    });
  }
  
  // Stop status polling
  void stopStatusPolling() {
    _statusTimer?.cancel();
  }
  
  // Ask a question
  Future<void> askQuestion(String question) async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      final response = await AssistantApiService.askQuestion(question);
      await refreshConversation();
      _error = null;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  // Refresh conversation history
  Future<void> refreshConversation() async {
    try {
      _conversation = await AssistantApiService.getConversation();
      _error = null;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }
  
  // Refresh statistics
  Future<void> refreshStats() async {
    try {
      _stats = await AssistantApiService.getStats();
      _error = null;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }
  
  // Reset conversation
  Future<void> resetConversation() async {
    _isLoading = true;
    _error = null;
    notifyListeners();
    
    try {
      await AssistantApiService.resetConversation();
      _conversation.clear();
      _status = null;
      await refreshStats();
      _error = null;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  @override
  void dispose() {
    _statusTimer?.cancel();
    super.dispose();
  }
}

// =============================================================================
// UI COMPONENTS EXAMPLE
// =============================================================================

class AssistantChatScreen extends StatefulWidget {
  @override
  _AssistantChatScreenState createState() => _AssistantChatScreenState();
}

class _AssistantChatScreenState extends State<AssistantChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  
  @override
  void initState() {
    super.initState();
    // Start status polling and load initial data
    final provider = Provider.of<AssistantProvider>(context, listen: false);
    provider.startStatusPolling();
    provider.refreshConversation();
    provider.refreshStats();
  }
  
  @override
  void dispose() {
    final provider = Provider.of<AssistantProvider>(context, listen: false);
    provider.stopStatusPolling();
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }
  
  void _sendMessage() async {
    final message = _messageController.text.trim();
    if (message.isEmpty) return;
    
    _messageController.clear();
    final provider = Provider.of<AssistantProvider>(context, listen: false);
    await provider.askQuestion(message);
    
    // Scroll to bottom
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('AI Assistant Chat'),
        actions: [
          Consumer<AssistantProvider>(
            builder: (context, provider, child) {
              return Row(
                children: [
                  Text('Q: ${provider.status?.questionCount ?? 0}'),
                  SizedBox(width: 8),
                  CircleAvatar(
                    radius: 6,
                    backgroundColor: _getStatusColor(provider.status?.status),
                  ),
                  SizedBox(width: 16),
                  IconButton(
                    icon: Icon(Icons.refresh),
                    onPressed: provider.refreshConversation,
                  ),
                  IconButton(
                    icon: Icon(Icons.clear_all),
                    onPressed: () => _showResetDialog(provider),
                  ),
                ],
              );
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Status bar
          Consumer<AssistantProvider>(
            builder: (context, provider, child) {
              if (provider.error != null) {
                return Container(
                  width: double.infinity,
                  color: Colors.red.shade100,
                  padding: EdgeInsets.all(8),
                  child: Text(
                    'Error: ${provider.error}',
                    style: TextStyle(color: Colors.red.shade800),
                  ),
                );
              }
              return SizedBox.shrink();
            },
          ),
          
          // Chat messages
          Expanded(
            child: Consumer<AssistantProvider>(
              builder: (context, provider, child) {
                if (provider.conversation.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.chat_bubble_outline, size: 64, color: Colors.grey),
                        SizedBox(height: 16),
                        Text(
                          'No conversation yet.\nAsk a question to get started!',
                          textAlign: TextAlign.center,
                          style: TextStyle(color: Colors.grey.shade600),
                        ),
                      ],
                    ),
                  );
                }
                
                return ListView.builder(
                  controller: _scrollController,
                  itemCount: provider.conversation.length,
                  itemBuilder: (context, index) {
                    final entry = provider.conversation[index];
                    return ChatBubble(
                      question: entry.question,
                      answer: entry.answer,
                      timestamp: entry.timestamp,
                    );
                  },
                );
              },
            ),
          ),
          
          // Loading indicator
          Consumer<AssistantProvider>(
            builder: (context, provider, child) {
              return provider.isLoading
                  ? LinearProgressIndicator()
                  : SizedBox.shrink();
            },
          ),
          
          // Input field
          Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 4)],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'Ask a question...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                      ),
                      contentPadding: EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 12,
                      ),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                    textInputAction: TextInputAction.send,
                  ),
                ),
                SizedBox(width: 8),
                Consumer<AssistantProvider>(
                  builder: (context, provider, child) {
                    return FloatingActionButton.small(
                      onPressed: provider.isLoading ? null : _sendMessage,
                      child: Icon(Icons.send),
                    );
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Color _getStatusColor(String? status) {
    switch (status) {
      case 'ready': return Colors.green;
      case 'processing': return Colors.orange;
      case 'error': return Colors.red;
      default: return Colors.grey;
    }
  }
  
  void _showResetDialog(AssistantProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Reset Conversation'),
        content: Text('This will clear all conversation history. Are you sure?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              provider.resetConversation();
            },
            child: Text('Reset'),
          ),
        ],
      ),
    );
  }
}

class ChatBubble extends StatelessWidget {
  final String question;
  final String answer;
  final DateTime timestamp;
  
  const ChatBubble({
    Key? key,
    required this.question,
    required this.answer,
    required this.timestamp,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // User question
          Align(
            alignment: Alignment.centerRight,
            child: Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Theme.of(context).primaryColor,
                borderRadius: BorderRadius.circular(18),
              ),
              child: Text(
                question,
                style: TextStyle(color: Colors.white),
              ),
            ),
          ),
          SizedBox(height: 8),
          
          // Assistant answer
          Align(
            alignment: Alignment.centerLeft,
            child: Container(
              padding: EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.grey.shade200,
                borderRadius: BorderRadius.circular(18),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(answer),
                  SizedBox(height: 4),
                  Text(
                    _formatTimestamp(timestamp),
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey.shade600,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
  
  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);
    
    if (difference.inSeconds < 60) {
      return 'Just now';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h ago';
    } else {
      return '${timestamp.day}/${timestamp.month} ${timestamp.hour}:${timestamp.minute.toString().padLeft(2, '0')}';
    }
  }
}

// =============================================================================
// USAGE EXAMPLE IN MAIN APP
// =============================================================================

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => AssistantProvider(),
      child: MaterialApp(
        title: 'AI Assistant Chat',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          visualDensity: VisualDensity.adaptivePlatformDensity,
        ),
        home: AssistantChatScreen(),
      ),
    );
  }
}

// =============================================================================
// PUBSPEC.YAML DEPENDENCIES NEEDED:
// =============================================================================
/*
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  provider: ^6.0.5

dev_dependencies:
  flutter_test:
    sdk: flutter
*/
