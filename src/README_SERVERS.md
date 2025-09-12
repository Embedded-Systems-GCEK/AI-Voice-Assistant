# 🚀 AI Voice Assistant - Multi-Server Startup Guide

## ⚡ Quick Start (Recommended)

### Windows Users - Choose One:

#### Option 1: PowerShell (Recommended)
```powershell
cd src
.\start_servers.ps1
```

#### Option 2: Command Prompt
```cmd
cd src
start_servers.bat
```

#### Option 3: Python Launcher
```bash
cd src
python launcher.py
```

## 📊 What Gets Started

| **Server** | **Port** | **Purpose** | **For Flutter** |
|------------|----------|-------------|-----------------|
| 🔥 **API Server** | **5001** | **Real-time assistant APIs** | **✅ PRIMARY** |
| 📦 Main Server | 5000 | Database & core APIs | Optional |
| 🌐 UI Server | 5002 | Web interface | Optional |

## 📱 Flutter Integration - USE THIS!

### Base URL for your Flutter app:
```
http://localhost:5001
```

### Key Endpoints:
- `GET /api/status` → Current question, answer, counters
- `POST /api/ask` → Send questions, get responses
- `GET /api/conversation` → Full chat history  
- `GET /api/example-questions` → Predefined questions
- `POST /api/reset` → Reset conversation

### Flutter HTTP Example:
```dart
class ApiService {
  static const baseUrl = 'http://localhost:5001';
  
  static Future<Map<String, dynamic>> askQuestion(String question) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/ask'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'question': question}),
    );
    return json.decode(response.body);
  }
  
  static Future<Map<String, dynamic>> getStatus() async {
    final response = await http.get(Uri.parse('$baseUrl/api/status'));
    return json.decode(response.body);
  }
}
```

## 🧪 Test Your Setup

```bash
# Test all endpoints
python launcher.py --test

# Get Flutter integration guide
python launcher.py --guide

# Manual test
curl http://localhost:5001/api/example-questions
```

## 📚 Documentation

- **Complete API Guide**: `API_GUIDE.md`
- **Flutter Integration**: `docs/FLUTTER_INTEGRATION_GUIDE.md`
- **Server Details**: Individual server folders

---

**🎯 For Flutter Development**: Just start the servers and use `http://localhost:5001` as your base URL!

**❓ Issues?** Check the individual terminal windows for detailed logs.
