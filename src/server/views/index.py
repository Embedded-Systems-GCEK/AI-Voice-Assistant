def index():
    return """
    <h1>AI Assistant Unified Server</h1>
    <p>This server provides both API and UI functionality.</p>
    <h3>Available Endpoints:</h3>
    <ul>
        <li><strong>Health:</strong> <a href="/health">/health</a></li>
        <li><strong>Statistics:</strong> <a href="/stats">/stats</a></li>
        <li><strong>API Example Questions:</strong> <a href="/api/example-questions">/api/example-questions</a></li>
        <li><strong>API Status:</strong> <a href="/api/assistant/status">/api/assistant/status</a></li>
    </ul>
    <h3>API Usage:</h3>
    <ul>
        <li><strong>POST /api/ask</strong> - Ask a question</li>
        <li><strong>GET /api/conversation/&lt;user_id&gt;</strong> - Get conversation history</li>
        <li><strong>POST /api/assistant/reset</strong> - Reset assistant</li>
    </ul>
    """