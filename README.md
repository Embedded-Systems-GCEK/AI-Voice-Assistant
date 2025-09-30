#  AI Voice Assistant 
This is a fully functional , generic AI powered Voice Assistant 


## Features 
### AI & Conversation
- **Multi-Provider AI Integration**: Supports Ollama (offline), GPT-5, Gemini, and Cohere AI 

> [!NOTE]
> You can also , implement your own **ai_provider** and pass to it.

- **Conversational Memory**: Maintains context throughout conversations
- **Intelligent Responses**: Answers questions using AI or fallback to predefined responses
- **Voice Feedback**: Text-to-speech output using Piper TTS engine

### REST API Server
- **Flask-based API**: Full RESTful API with JSON responses
- **Database Integration**: SQLite database with SQLAlchemy for data persistence
- **User Management**: User tracking and conversation history
- **CORS Support**: Cross-origin requests enabled for web/mobile clients
- **API Documentation**: Interactive Swagger UI documentation available at `/apidocs`

### Mobile Integration
- **Flutter App Support**: Designed for seamless integration with Flutter mobile applications
- **Real-time Communication**: API endpoints for live assistant interaction
- **Example Questions**: Pre-configured question sets for mobile app demonstration


## API Documentation

The API includes comprehensive Swagger/OpenAPI documentation that can be accessed when the server is running:

1. Start the server: `python src/app.py`
2. Open your browser and navigate to: `http://localhost:5000/apidocs`
3. The interactive documentation allows you to:
   - View all available endpoints
   - See request/response schemas
   - Test API calls directly from the browser
   - Download the OpenAPI specification

### Key Endpoints Documented:
- **Health Check**: `/health` - Server health status
- **User Management**: `/users` - CRUD operations for users
- **AI Assistant**: `/api/ask` - Ask questions to the AI assistant
- **Conversations**: `/api/conversation/<user_id>` - Get user conversation history
- **Example Questions**: `/api/example-questions` - Pre-configured question sets


## 🤝 Contributing

This project is developed by the UI team at Government College of Engineering Kannur for the APCI 2025 conference. Contributions are welcome!

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Run `python test_setup.py` to verify your setup
4. Make your changes
5. Test with both `python demo.py` and full voice mode
6. Submit a pull request