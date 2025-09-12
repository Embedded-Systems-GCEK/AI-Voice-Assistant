#!/usr/bin/env python3
"""
Multi-Server Launcher for AI Voice Assistant
Starts all necessary servers for complete Flutter integration
"""

import subprocess
import threading
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import webbrowser

def run_server(name, command, port, color_code=""):
    """Run a server in a separate process"""
    print(f"{color_code}🚀 Starting {name} on port {port}...{color_code}")
    try:
        # Use shell=True on Windows for proper PowerShell execution
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print(f"{color_code}✅ {name} started with PID {process.pid}{color_code}")
        
        # Print output in real-time
        for line in process.stdout:
            print(f"{color_code}[{name}] {line.rstrip()}{color_code}")
            
        process.wait()
        print(f"{color_code}❌ {name} stopped{color_code}")
        
    except Exception as e:
        print(f"{color_code}❌ Failed to start {name}: {e}{color_code}")

def start_all_servers():
    """Start all servers concurrently"""
    
    print("=" * 60)
    print("🤖 AI VOICE ASSISTANT - MULTI-SERVER LAUNCHER")
    print("=" * 60)
    print()
    
    servers = [
        {
            "name": "API Server",
            "command": f"{sys.executable} api_server.py",
            "port": 5001,
            "color": "\033[92m"  # Green
        },
        {
            "name": "Main Server", 
            "command": f"{sys.executable} server/server.py",
            "port": 5000,
            "color": "\033[94m"  # Blue
        },
        {
            "name": "UI Server",
            "command": f"{sys.executable} ui/server.py", 
            "port": 5002,
            "color": "\033[96m"  # Cyan
        }
    ]
    
    print("📋 Server Configuration:")
    for server in servers:
        print(f"   • {server['name']:<15} → http://localhost:{server['port']}")
    print()
    
    print("🔗 Flutter Integration Endpoints:")
    print("   • Main API:      http://localhost:5001/api/")
    print("   • Server API:    http://localhost:5000/api/")
    print("   • UI API:        http://localhost:5002/api/")
    print()
    
    print("📱 Flutter App Usage:")
    print("   • Use http://localhost:5001 as your base URL")
    print("   • Available endpoints:")
    print("     - GET  /api/status           → Assistant status & current Q&A")
    print("     - POST /api/ask              → Ask questions")
    print("     - GET  /api/conversation     → Get conversation history")
    print("     - GET  /api/stats            → Get statistics")
    print("     - GET  /api/example-questions → Get example questions")
    print("     - POST /api/reset            → Reset conversation")
    print()
    
    print("⏳ Starting servers (this may take a moment)...")
    print("-" * 60)
    
    # Start servers using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=len(servers)) as executor:
        futures = []
        
        for server in servers:
            future = executor.submit(
                run_server,
                server["name"],
                server["command"], 
                server["port"],
                server["color"]
            )
            futures.append(future)
            time.sleep(2)  # Stagger startup
        
        try:
            print("\n🎯 All servers are starting...")
            print("📖 Press Ctrl+C to stop all servers")
            print("-" * 60)
            
            # Wait for all servers
            for future in futures:
                future.result()
                
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down all servers...")
            # The processes will be terminated when the main process exits

def test_api_endpoints():
    """Test the API endpoints with sample requests"""
    import requests
    import json
    
    base_url = "http://localhost:5001"
    
    print("\n🧪 Testing API Endpoints...")
    print("-" * 40)
    
    # Wait for server to be ready
    print("⏳ Waiting for API server...")
    for _ in range(30):  # Wait up to 30 seconds
        try:
            response = requests.get(f"{base_url}/health", timeout=1)
            if response.status_code == 200:
                print("✅ API server is ready!")
                break
        except:
            time.sleep(1)
    else:
        print("❌ API server not responding")
        return
    
    # Test endpoints
    tests = [
        ("GET", "/", "Server info"),
        ("GET", "/api/status", "Assistant status"),
        ("GET", "/api/example-questions", "Example questions"),
        ("GET", "/api/stats", "Statistics"),
        ("POST", "/api/ask", "Ask question", {"question": "What time is it?"}),
        ("GET", "/api/conversation", "Conversation history"),
    ]
    
    for method, endpoint, description, *data in tests:
        try:
            url = f"{base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=5)
            elif method == "POST":
                payload = data[0] if data else {}
                response = requests.post(url, json=payload, timeout=5)
            
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"{status_icon} {description:<20} [{method}] {endpoint} → {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'data' in result:
                    print(f"   └── Data keys: {list(result['data'].keys())}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ {description:<20} [{method}] {endpoint} → Error: {e}")
        
        time.sleep(0.5)

def show_flutter_integration_guide():
    """Show Flutter integration instructions"""
    
    guide = '''
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
    '''
    
    print(guide)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            test_api_endpoints()
        elif sys.argv[1] == '--guide':
            show_flutter_integration_guide()
        else:
            print("Usage:")
            print("  python launcher.py         # Start all servers")
            print("  python launcher.py --test  # Test API endpoints")
            print("  python launcher.py --guide # Show Flutter guide")
    else:
        try:
            start_all_servers()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
