# AI Voice Assistant API Usage Templates

This directory contains comprehensive API integration templates for different programming languages and frameworks to help you quickly integrate with the AI Voice Assistant API.

## 📋 Available Templates

### 1. **Flutter/Dart Template** (`flutter_dart_template.dart`)
- Complete Flutter app implementation with Provider state management
- Real-time status updates and chat interface
- Ready-to-use widgets and API service classes
- Example screens and UI components

### 2. **JavaScript/Node.js Template** (`javascript_template.js`)
- Works in both browser and Node.js environments
- React hooks and vanilla JavaScript examples
- Express.js middleware for server integration
- WebSocket-style real-time updates

### 3. **Python Template** (`python_template.py`)
- Synchronous and asynchronous API clients
- Flask and FastAPI integration examples
- Command-line interface implementation
- Complete data models and error handling

### 4. **C# Template** (`csharp_template.cs`)
- .NET/C# implementation with HttpClient
- WPF MVVM example with data binding
- ASP.NET Core controller integration
- Console application example

## 🚀 Quick Start

### Base API URLs
```
Primary API (Flutter):  http://localhost:5001
Unified Server:         http://localhost:5000
```

### Core Endpoints
- `GET /api/status` - Current assistant status & Q&A info
- `POST /api/ask` - Send questions and get responses
- `GET /api/conversation` - Full conversation history
- `GET /api/stats` - Usage statistics
- `GET /api/example-questions` - Predefined questions
- `POST /api/reset` - Reset conversation state

## 🎯 Template Features

Each template includes:
- ✅ **Complete API Client** - Full HTTP client implementation
- ✅ **Error Handling** - Comprehensive error management
- ✅ **Real-time Updates** - Status polling and live data
- ✅ **Data Models** - Strongly-typed response objects
- ✅ **Examples** - Working code samples and usage patterns
- ✅ **UI Components** - Ready-to-use interface elements
- ✅ **Documentation** - Inline comments and usage instructions

## 📱 Flutter Integration (Recommended)

For Flutter apps, use the `flutter_dart_template.dart`:

```dart
// Basic usage
final client = AssistantApiService();
final response = await client.askQuestion("What time is it?");
print(response['data']['answer']);

// Real-time status
final provider = AssistantProvider();
provider.startStatusPolling();
```

## 🌐 Web Integration

For web apps, use the `javascript_template.js`:

```javascript
// Basic usage
const client = new AssistantApiClient();
const response = await client.askQuestion("What time is it?");
console.log(response.answer);

// React integration
const { status, conversation, askQuestion } = useAssistantApi();
```

## 🐍 Python Integration

For Python apps, use the `python_template.py`:

```python
# Basic usage
client = AssistantApiClient()
response = client.ask_question("What time is it?")
print(response.answer)

# Async usage
async_client = AsyncAssistantApiClient()
response = await async_client.ask_question("What time is it?")
```

## 🔧 C# Integration

For .NET apps, use the `csharp_template.cs`:

```csharp
// Basic usage
var client = new AssistantApiClient();
var response = await client.AskQuestionAsync("What time is it?");
Console.WriteLine(response.Answer);
```

## 🛠️ Server Setup

Before using any template, make sure the AI Assistant servers are running:

```bash
# Option 1: Use the unified launcher (recommended)
cd src
python launcher.py

# Option 2: Use PowerShell script
.\start_servers.ps1

# Option 3: Use batch script
start_servers.bat

# Option 4: Start servers manually
# Terminal 1: API Server (for Flutter)
python api_server.py

# Terminal 2: Unified Server (for web UI)
python server/server.py
```

## 📊 Response Format

All API endpoints return standardized JSON responses:

```json
{
  "status": "success",
  "data": {
    // Endpoint-specific data
  },
  "message": "Optional message"
}
```

## 🔍 Testing Your Integration

Each template includes testing examples. You can also test manually:

```bash
# Test the API server
curl http://localhost:5001/api/status

# Ask a question
curl -X POST http://localhost:5001/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What time is it?"}'
```

## 🚨 Error Handling

All templates include comprehensive error handling for:
- Network connectivity issues
- API server unavailability
- Invalid responses
- Timeout scenarios
- Rate limiting (if implemented)

## 🔄 Real-time Features

Each template supports real-time features:
- **Status Polling** - Regular updates of assistant status
- **Live Conversation** - Automatic refresh of conversation history
- **Error Recovery** - Automatic retry and reconnection
- **State Synchronization** - Keep UI in sync with API state

## 📚 Additional Resources

- **API Documentation**: `../API_GUIDE.md`
- **Flutter Guide**: `../docs/FLUTTER_INTEGRATION_GUIDE.md`
- **Server Setup**: `../src/launcher.py --guide`
- **Testing**: `../src/launcher.py --test`

## 🏗️ Architecture

The AI Assistant now runs on a **simplified 2-server architecture**:

1. **API Server (Port 5001)** - Optimized for Flutter/mobile apps
   - Lightweight and fast responses
   - Real-time status updates
   - Mobile-friendly JSON responses

2. **Unified Server (Port 5000)** - Web UI and general API access  
   - Includes both API functionality and web interface
   - Database operations and user management
   - Comprehensive statistics and analytics
   - Web-friendly HTML responses for browsers

**Previous 3-server setup was consolidated** - The separate UI server was redundant and has been merged with the main server for better efficiency.

## 🤝 Contributing

To add a new template:
1. Create a new file: `{language}_template.{ext}`
2. Follow the existing template structure
3. Include all core API methods
4. Add practical usage examples
5. Include error handling and real-time features

---

**Need Help?**
- Check the main `API_GUIDE.md` for detailed documentation
- Run `python src/launcher.py --guide` for interactive help
- Test your integration with `python src/launcher.py --test`
