/**
 * AI Voice Assistant - JavaScript/Node.js API Integration Template
 * Complete implementation example for web and Node.js applications
 */

// =============================================================================
// API CLIENT CLASS (Works in Browser and Node.js)
// =============================================================================

class AssistantApiClient {
    constructor(baseUrl = 'http://localhost:5001', timeout = 30000) {
        this.baseUrl = baseUrl;
        this.timeout = timeout;
        this.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
    }

    // Helper method for making HTTP requests
    async _makeRequest(method, endpoint, data = null) {
        const url = `${this.baseUrl}${endpoint}`;
        const options = {
            method,
            headers: this.headers,
            signal: AbortSignal.timeout(this.timeout)
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            
            if (result.status === 'error') {
                throw new Error(result.message || 'API Error');
            }

            return result;
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            throw error;
        }
    }

    // GET /api/status - Get current assistant status
    async getStatus() {
        const response = await this._makeRequest('GET', '/api/status');
        return response.data;
    }

    // POST /api/ask - Ask a question
    async askQuestion(question, userId = null) {
        const data = { question };
        if (userId) data.user_id = userId;
        
        const response = await this._makeRequest('POST', '/api/ask', data);
        return response.data;
    }

    // GET /api/conversation - Get conversation history
    async getConversation(options = {}) {
        const { userId, limit } = options;
        const params = new URLSearchParams();
        
        if (userId) params.append('user_id', userId);
        if (limit) params.append('limit', limit.toString());
        
        const endpoint = params.toString() ? 
            `/api/conversation?${params.toString()}` : 
            '/api/conversation';
            
        const response = await this._makeRequest('GET', endpoint);
        return response.data.conversation;
    }

    // GET /api/stats - Get statistics
    async getStats() {
        const response = await this._makeRequest('GET', '/api/stats');
        return response.data;
    }

    // GET /api/example-questions - Get example questions
    async getExampleQuestions(category = null) {
        const endpoint = category ? 
            `/api/example-questions?category=${encodeURIComponent(category)}` : 
            '/api/example-questions';
            
        const response = await this._makeRequest('GET', endpoint);
        return response.data;
    }

    // POST /api/reset - Reset conversation
    async resetConversation() {
        const response = await this._makeRequest('POST', '/api/reset');
        return response.data;
    }

    // GET /health - Health check
    async checkHealth() {
        try {
            const response = await this._makeRequest('GET', '/health');
            return true;
        } catch (error) {
            return false;
        }
    }

    // Start real-time status polling
    startStatusPolling(callback, interval = 2000) {
        const poll = async () => {
            try {
                const status = await this.getStatus();
                callback(null, status);
            } catch (error) {
                callback(error, null);
            }
        };

        // Initial poll
        poll();
        
        // Set up interval
        const intervalId = setInterval(poll, interval);
        
        // Return function to stop polling
        return () => clearInterval(intervalId);
    }
}

// =============================================================================
// REACT.JS INTEGRATION EXAMPLE
// =============================================================================

// React Hook for Assistant API
function useAssistantApi() {
    const [client] = React.useState(() => new AssistantApiClient());
    const [status, setStatus] = React.useState(null);
    const [conversation, setConversation] = React.useState([]);
    const [stats, setStats] = React.useState(null);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState(null);

    // Start status polling
    React.useEffect(() => {
        const stopPolling = client.startStatusPolling((error, newStatus) => {
            if (error) {
                setError(error.message);
            } else {
                setStatus(newStatus);
                setError(null);
            }
        });

        return stopPolling;
    }, [client]);

    // Load initial data
    React.useEffect(() => {
        loadConversation();
        loadStats();
    }, []);

    const loadConversation = async () => {
        try {
            const conv = await client.getConversation();
            setConversation(conv);
            setError(null);
        } catch (err) {
            setError(err.message);
        }
    };

    const loadStats = async () => {
        try {
            const s = await client.getStats();
            setStats(s);
            setError(null);
        } catch (err) {
            setError(err.message);
        }
    };

    const askQuestion = async (question) => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await client.askQuestion(question);
            await loadConversation(); // Refresh conversation
            await loadStats(); // Refresh stats
            return response;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const resetConversation = async () => {
        setLoading(true);
        setError(null);
        
        try {
            await client.resetConversation();
            setConversation([]);
            await loadStats();
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return {
        client,
        status,
        conversation,
        stats,
        loading,
        error,
        askQuestion,
        resetConversation,
        loadConversation,
        loadStats
    };
}

// React Chat Component
function AssistantChat() {
    const {
        status,
        conversation,
        stats,
        loading,
        error,
        askQuestion,
        resetConversation
    } = useAssistantApi();

    const [message, setMessage] = React.useState('');
    const messagesEndRef = React.useRef(null);

    // Auto-scroll to bottom
    React.useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [conversation]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!message.trim()) return;

        const questionText = message;
        setMessage('');

        try {
            await askQuestion(questionText);
        } catch (err) {
            console.error('Failed to ask question:', err);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'ready': return '#4CAF50';
            case 'processing': return '#FF9800';
            case 'error': return '#F44336';
            default: return '#9E9E9E';
        }
    };

    return React.createElement('div', { className: 'chat-container' }, [
        // Header
        React.createElement('div', { 
            key: 'header',
            className: 'chat-header',
            style: { 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                padding: '1rem',
                borderBottom: '1px solid #eee'
            }
        }, [
            React.createElement('h2', { key: 'title' }, 'AI Assistant Chat'),
            React.createElement('div', { 
                key: 'status',
                style: { display: 'flex', alignItems: 'center', gap: '1rem' }
            }, [
                React.createElement('span', { key: 'count' }, `Questions: ${stats?.total_questions || 0}`),
                React.createElement('div', {
                    key: 'indicator',
                    style: {
                        width: '12px',
                        height: '12px',
                        borderRadius: '50%',
                        backgroundColor: getStatusColor(status?.assistant_status)
                    }
                }),
                React.createElement('button', {
                    key: 'reset',
                    onClick: resetConversation,
                    disabled: loading,
                    style: { padding: '0.5rem 1rem', marginLeft: '1rem' }
                }, 'Reset')
            ])
        ]),

        // Error display
        error && React.createElement('div', {
            key: 'error',
            style: {
                backgroundColor: '#ffebee',
                color: '#c62828',
                padding: '1rem',
                margin: '1rem'
            }
        }, `Error: ${error}`),

        // Messages
        React.createElement('div', {
            key: 'messages',
            className: 'messages',
            style: {
                flex: 1,
                overflowY: 'auto',
                padding: '1rem',
                maxHeight: '500px'
            }
        }, [
            ...conversation.map((entry, index) => 
                React.createElement('div', { 
                    key: index,
                    style: { marginBottom: '1rem' }
                }, [
                    // User question
                    React.createElement('div', {
                        key: 'question',
                        style: {
                            textAlign: 'right',
                            marginBottom: '0.5rem'
                        }
                    }, React.createElement('div', {
                        style: {
                            display: 'inline-block',
                            backgroundColor: '#2196F3',
                            color: 'white',
                            padding: '0.5rem 1rem',
                            borderRadius: '18px',
                            maxWidth: '70%'
                        }
                    }, entry.question)),

                    // Assistant answer
                    React.createElement('div', {
                        key: 'answer',
                        style: {
                            textAlign: 'left'
                        }
                    }, React.createElement('div', {
                        style: {
                            display: 'inline-block',
                            backgroundColor: '#f5f5f5',
                            padding: '0.5rem 1rem',
                            borderRadius: '18px',
                            maxWidth: '70%'
                        }
                    }, [
                        React.createElement('div', { key: 'text' }, entry.answer),
                        React.createElement('div', {
                            key: 'time',
                            style: {
                                fontSize: '0.8rem',
                                color: '#666',
                                marginTop: '0.25rem'
                            }
                        }, new Date(entry.timestamp).toLocaleTimeString())
                    ]))
                ])
            ),
            React.createElement('div', { 
                key: 'end',
                ref: messagesEndRef 
            })
        ]),

        // Loading indicator
        loading && React.createElement('div', {
            key: 'loading',
            style: {
                padding: '1rem',
                textAlign: 'center',
                color: '#666'
            }
        }, 'Processing...'),

        // Input form
        React.createElement('form', {
            key: 'form',
            onSubmit: handleSubmit,
            style: {
                display: 'flex',
                padding: '1rem',
                borderTop: '1px solid #eee',
                gap: '0.5rem'
            }
        }, [
            React.createElement('input', {
                key: 'input',
                type: 'text',
                value: message,
                onChange: (e) => setMessage(e.target.value),
                placeholder: 'Ask a question...',
                disabled: loading,
                style: {
                    flex: 1,
                    padding: '0.75rem',
                    border: '1px solid #ddd',
                    borderRadius: '24px',
                    outline: 'none'
                }
            }),
            React.createElement('button', {
                key: 'submit',
                type: 'submit',
                disabled: loading || !message.trim(),
                style: {
                    padding: '0.75rem 1.5rem',
                    backgroundColor: '#2196F3',
                    color: 'white',
                    border: 'none',
                    borderRadius: '24px',
                    cursor: loading ? 'not-allowed' : 'pointer'
                }
            }, 'Send')
        ])
    ]);
}

// =============================================================================
// VANILLA JAVASCRIPT EXAMPLE
// =============================================================================

class VanillaChatApp {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.client = new AssistantApiClient();
        this.conversation = [];
        this.status = null;
        
        this.init();
    }

    init() {
        this.render();
        this.startStatusPolling();
        this.loadInitialData();
    }

    render() {
        this.container.innerHTML = `
            <div class="chat-app">
                <div class="chat-header">
                    <h2>AI Assistant Chat</h2>
                    <div class="status-info">
                        <span id="question-count">Questions: 0</span>
                        <div id="status-indicator" class="status-indicator"></div>
                        <button id="reset-btn" class="reset-btn">Reset</button>
                    </div>
                </div>
                <div id="error-display" class="error-display" style="display: none;"></div>
                <div id="messages" class="messages"></div>
                <div id="loading" class="loading" style="display: none;">Processing...</div>
                <form id="message-form" class="message-form">
                    <input type="text" id="message-input" placeholder="Ask a question..." />
                    <button type="submit">Send</button>
                </form>
            </div>
        `;

        // Add event listeners
        document.getElementById('message-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        document.getElementById('reset-btn').addEventListener('click', () => {
            this.resetConversation();
        });
    }

    startStatusPolling() {
        this.client.startStatusPolling((error, status) => {
            if (error) {
                this.showError(error.message);
            } else {
                this.status = status;
                this.updateStatusDisplay();
            }
        });
    }

    async loadInitialData() {
        try {
            const [conversation, stats] = await Promise.all([
                this.client.getConversation(),
                this.client.getStats()
            ]);
            
            this.conversation = conversation;
            this.updateMessagesDisplay();
            this.updateStatsDisplay(stats);
        } catch (error) {
            this.showError(error.message);
        }
    }

    async sendMessage() {
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        
        if (!message) return;

        input.value = '';
        this.showLoading(true);

        try {
            await this.client.askQuestion(message);
            
            // Refresh conversation
            this.conversation = await this.client.getConversation();
            this.updateMessagesDisplay();
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async resetConversation() {
        this.showLoading(true);
        
        try {
            await this.client.resetConversation();
            this.conversation = [];
            this.updateMessagesDisplay();
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    updateMessagesDisplay() {
        const messagesDiv = document.getElementById('messages');
        
        if (this.conversation.length === 0) {
            messagesDiv.innerHTML = `
                <div class="empty-state">
                    <p>No conversation yet. Ask a question to get started!</p>
                </div>
            `;
            return;
        }

        messagesDiv.innerHTML = this.conversation
            .map(entry => `
                <div class="message-pair">
                    <div class="user-message">
                        <div class="message-bubble user">${this.escapeHtml(entry.question)}</div>
                    </div>
                    <div class="assistant-message">
                        <div class="message-bubble assistant">
                            ${this.escapeHtml(entry.answer)}
                            <div class="timestamp">${new Date(entry.timestamp).toLocaleTimeString()}</div>
                        </div>
                    </div>
                </div>
            `)
            .join('');

        // Scroll to bottom
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    updateStatusDisplay() {
        const indicator = document.getElementById('status-indicator');
        if (!indicator || !this.status) return;

        const colors = {
            'ready': '#4CAF50',
            'processing': '#FF9800',
            'error': '#F44336'
        };

        indicator.style.backgroundColor = colors[this.status.assistant_status] || '#9E9E9E';
    }

    updateStatsDisplay(stats) {
        const countEl = document.getElementById('question-count');
        if (countEl) {
            countEl.textContent = `Questions: ${stats.total_questions}`;
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('error-display');
        errorDiv.textContent = `Error: ${message}`;
        errorDiv.style.display = 'block';
        
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }

    showLoading(show) {
        const loadingDiv = document.getElementById('loading');
        loadingDiv.style.display = show ? 'block' : 'none';
        
        const submitBtn = document.querySelector('#message-form button');
        submitBtn.disabled = show;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// =============================================================================
// NODE.JS EXPRESS MIDDLEWARE EXAMPLE
// =============================================================================

// Example Express.js middleware for proxying requests
function createAssistantProxy(assistantApiUrl = 'http://localhost:5001') {
    const client = new AssistantApiClient(assistantApiUrl);
    
    return {
        // Middleware to check assistant health
        healthCheck: async (req, res, next) => {
            try {
                const isHealthy = await client.checkHealth();
                if (isHealthy) {
                    next();
                } else {
                    res.status(503).json({ error: 'Assistant service unavailable' });
                }
            } catch (error) {
                res.status(503).json({ error: 'Assistant service error' });
            }
        },

        // Route handlers
        getStatus: async (req, res) => {
            try {
                const status = await client.getStatus();
                res.json(status);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        },

        askQuestion: async (req, res) => {
            try {
                const { question, user_id } = req.body;
                const response = await client.askQuestion(question, user_id);
                res.json(response);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        },

        getConversation: async (req, res) => {
            try {
                const { user_id, limit } = req.query;
                const conversation = await client.getConversation({ 
                    userId: user_id, 
                    limit: limit ? parseInt(limit) : undefined 
                });
                res.json(conversation);
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        }
    };
}

// =============================================================================
// CSS STYLES FOR VANILLA JS EXAMPLE
// =============================================================================

const CSS_STYLES = `
.chat-app {
    max-width: 800px;
    margin: 0 auto;
    height: 600px;
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f5f5f5;
    border-bottom: 1px solid #ddd;
}

.status-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #9E9E9E;
}

.reset-btn {
    padding: 0.5rem 1rem;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.error-display {
    background-color: #ffebee;
    color: #c62828;
    padding: 1rem;
    margin: 1rem;
    border-radius: 4px;
}

.messages {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}

.empty-state {
    text-align: center;
    color: #666;
    margin-top: 2rem;
}

.message-pair {
    margin-bottom: 1rem;
}

.user-message {
    text-align: right;
    margin-bottom: 0.5rem;
}

.assistant-message {
    text-align: left;
}

.message-bubble {
    display: inline-block;
    max-width: 70%;
    padding: 0.75rem 1rem;
    border-radius: 18px;
    word-wrap: break-word;
}

.message-bubble.user {
    background-color: #2196F3;
    color: white;
}

.message-bubble.assistant {
    background-color: #f5f5f5;
    color: #333;
}

.timestamp {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.25rem;
}

.loading {
    text-align: center;
    padding: 1rem;
    color: #666;
}

.message-form {
    display: flex;
    padding: 1rem;
    border-top: 1px solid #ddd;
    gap: 0.5rem;
}

.message-form input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 24px;
    outline: none;
}

.message-form button {
    padding: 0.75rem 1.5rem;
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 24px;
    cursor: pointer;
}

.message-form button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
`;

// =============================================================================
// USAGE EXAMPLES
// =============================================================================

// Simple usage example
async function simpleExample() {
    const client = new AssistantApiClient();
    
    try {
        // Check if assistant is available
        const isHealthy = await client.checkHealth();
        console.log('Assistant available:', isHealthy);
        
        // Get current status
        const status = await client.getStatus();
        console.log('Current status:', status);
        
        // Ask a question
        const response = await client.askQuestion('What time is it?');
        console.log('Response:', response);
        
        // Get conversation history
        const conversation = await client.getConversation();
        console.log('Conversation:', conversation);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Initialize vanilla JS app
function initVanillaApp() {
    // Add CSS
    const style = document.createElement('style');
    style.textContent = CSS_STYLES;
    document.head.appendChild(style);
    
    // Create app
    const app = new VanillaChatApp('chat-container');
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AssistantApiClient,
        createAssistantProxy,
        VanillaChatApp
    };
}

// Export for ES modules
if (typeof window === 'undefined') {
    export {
        AssistantApiClient,
        createAssistantProxy,
        VanillaChatApp
    };
}
