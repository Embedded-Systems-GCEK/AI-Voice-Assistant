/* AI Voice Assistant - C# API Integration Template
 * Complete implementation example for .NET applications
 */

using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Threading;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace AIAssistantClient
{
    // =============================================================================
    // DATA MODELS
    // =============================================================================
    
    public class AssistantStatus
    {
        public string AssistantStatusValue { get; set; } = "";
        public bool AssistantAvailable { get; set; }
        public string CurrentQuestion { get; set; } = "";
        public string CurrentAnswer { get; set; } = "";
        public int QuestionCount { get; set; }
        public string SessionId { get; set; } = "";
        public int ConversationLength { get; set; }
        public DateTime Timestamp { get; set; }
    }

    public class QuestionResponse
    {
        public string Question { get; set; } = "";
        public string Answer { get; set; } = "";
        public int QuestionNumber { get; set; }
        public DateTime Timestamp { get; set; }
        public string SessionId { get; set; } = "";
    }

    public class ConversationEntry
    {
        public int Id { get; set; }
        public string Question { get; set; } = "";
        public string Answer { get; set; } = "";
        public DateTime Timestamp { get; set; }
        public string UserId { get; set; } = "";
        public string SessionId { get; set; } = "";
    }

    public class AssistantStats
    {
        public int TotalQuestions { get; set; }
        public int ConversationEntries { get; set; }
        public string SessionId { get; set; } = "";
        public string AssistantStatusValue { get; set; } = "";
        public DateTime Uptime { get; set; }
    }

    public class ExampleQuestion
    {
        public int Id { get; set; }
        public string Category { get; set; } = "";
        public string Question { get; set; } = "";
        public string Description { get; set; } = "";
    }

    public class ApiResponse<T>
    {
        public string Status { get; set; } = "";
        public T Data { get; set; }
        public string Message { get; set; } = "";
    }

    // =============================================================================
    // HTTP CLIENT
    // =============================================================================

    public class AssistantApiClient : IDisposable
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private Timer _statusTimer;

        public event EventHandler<AssistantStatus> StatusUpdated;
        public event EventHandler<string> ErrorOccurred;

        public AssistantApiClient(string baseUrl = "http://localhost:5001", TimeSpan? timeout = null)
        {
            _baseUrl = baseUrl.TrimEnd('/');
            _httpClient = new HttpClient
            {
                Timeout = timeout ?? TimeSpan.FromSeconds(30)
            };
            _httpClient.DefaultRequestHeaders.Add("Accept", "application/json");
        }

        // Helper method for making requests
        private async Task<ApiResponse<T>> MakeRequestAsync<T>(HttpMethod method, string endpoint, object data = null)
        {
            var url = $"{_baseUrl}{endpoint}";
            var request = new HttpRequestMessage(method, url);

            if (data != null)
            {
                var json = JsonSerializer.Serialize(data);
                request.Content = new StringContent(json, Encoding.UTF8, "application/json");
            }

            try
            {
                var response = await _httpClient.SendAsync(request);
                response.EnsureSuccessStatusCode();

                var responseContent = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<ApiResponse<T>>(responseContent, new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                });

                if (result.Status == "error")
                {
                    throw new Exception(result.Message ?? "API Error");
                }

                return result;
            }
            catch (HttpRequestException ex)
            {
                throw new Exception($"HTTP request failed: {ex.Message}", ex);
            }
            catch (TaskCanceledException ex)
            {
                throw new Exception("Request timeout", ex);
            }
            catch (JsonException ex)
            {
                throw new Exception($"Invalid JSON response: {ex.Message}", ex);
            }
        }

        // API Methods
        public async Task<AssistantStatus> GetStatusAsync()
        {
            var response = await MakeRequestAsync<AssistantStatus>(HttpMethod.Get, "/api/status");
            return response.Data;
        }

        public async Task<QuestionResponse> AskQuestionAsync(string question, string userId = null)
        {
            var data = new { question, user_id = userId };
            var response = await MakeRequestAsync<QuestionResponse>(HttpMethod.Post, "/api/ask", data);
            return response.Data;
        }

        public async Task<List<ConversationEntry>> GetConversationAsync(string userId = null, int? limit = null)
        {
            var queryParams = new List<string>();
            if (!string.IsNullOrEmpty(userId))
                queryParams.Add($"user_id={Uri.EscapeDataString(userId)}");
            if (limit.HasValue)
                queryParams.Add($"limit={limit.Value}");

            var endpoint = "/api/conversation";
            if (queryParams.Count > 0)
                endpoint += "?" + string.Join("&", queryParams);

            var response = await MakeRequestAsync<ConversationResponse>(HttpMethod.Get, endpoint);
            return response.Data.Conversation;
        }

        public async Task<AssistantStats> GetStatsAsync()
        {
            var response = await MakeRequestAsync<AssistantStats>(HttpMethod.Get, "/api/stats");
            return response.Data;
        }

        public async Task<List<ExampleQuestion>> GetExampleQuestionsAsync(string category = null)
        {
            var endpoint = "/api/example-questions";
            if (!string.IsNullOrEmpty(category))
                endpoint += $"?category={Uri.EscapeDataString(category)}";

            var response = await MakeRequestAsync<ExampleQuestionsResponse>(HttpMethod.Get, endpoint);
            return response.Data.Questions;
        }

        public async Task<ResetResponse> ResetConversationAsync()
        {
            var response = await MakeRequestAsync<ResetResponse>(HttpMethod.Post, "/api/reset");
            return response.Data;
        }

        public async Task<bool> CheckHealthAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync($"{_baseUrl}/health");
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        // Status polling
        public void StartStatusPolling(TimeSpan interval)
        {
            _statusTimer?.Dispose();
            _statusTimer = new Timer(async _ =>
            {
                try
                {
                    var status = await GetStatusAsync();
                    StatusUpdated?.Invoke(this, status);
                }
                catch (Exception ex)
                {
                    ErrorOccurred?.Invoke(this, ex.Message);
                }
            }, null, TimeSpan.Zero, interval);
        }

        public void StopStatusPolling()
        {
            _statusTimer?.Dispose();
            _statusTimer = null;
        }

        public void Dispose()
        {
            _statusTimer?.Dispose();
            _httpClient?.Dispose();
        }

        // Helper classes for deserialization
        private class ConversationResponse
        {
            public List<ConversationEntry> Conversation { get; set; } = new();
        }

        private class ExampleQuestionsResponse
        {
            public List<ExampleQuestion> Questions { get; set; } = new();
            public List<string> Categories { get; set; } = new();
        }

        private class ResetResponse
        {
            public string SessionId { get; set; } = "";
            public DateTime Timestamp { get; set; }
        }
    }

    // =============================================================================
    // WPF VIEWMODEL EXAMPLE
    // =============================================================================

    public class ChatViewModel : INotifyPropertyChanged
    {
        private readonly AssistantApiClient _apiClient;
        private AssistantStatus _status;
        private string _currentMessage = "";
        private bool _isLoading = false;
        private string _errorMessage = "";
        private List<ConversationEntry> _conversation = new();

        public ChatViewModel(string apiUrl = "http://localhost:5001")
        {
            _apiClient = new AssistantApiClient(apiUrl);
            _apiClient.StatusUpdated += OnStatusUpdated;
            _apiClient.ErrorOccurred += OnErrorOccurred;

            SendMessageCommand = new RelayCommand(async () => await SendMessageAsync(), () => !IsLoading && !string.IsNullOrWhiteSpace(CurrentMessage));
            ResetConversationCommand = new RelayCommand(async () => await ResetConversationAsync(), () => !IsLoading);
            RefreshCommand = new RelayCommand(async () => await RefreshDataAsync(), () => !IsLoading);

            _ = InitializeAsync();
        }

        // Properties
        public AssistantStatus Status
        {
            get => _status;
            private set { _status = value; OnPropertyChanged(); }
        }

        public string CurrentMessage
        {
            get => _currentMessage;
            set
            {
                _currentMessage = value;
                OnPropertyChanged();
                SendMessageCommand.RaiseCanExecuteChanged();
            }
        }

        public bool IsLoading
        {
            get => _isLoading;
            private set
            {
                _isLoading = value;
                OnPropertyChanged();
                SendMessageCommand.RaiseCanExecuteChanged();
                ResetConversationCommand.RaiseCanExecuteChanged();
                RefreshCommand.RaiseCanExecuteChanged();
            }
        }

        public string ErrorMessage
        {
            get => _errorMessage;
            private set { _errorMessage = value; OnPropertyChanged(); }
        }

        public List<ConversationEntry> Conversation
        {
            get => _conversation;
            private set { _conversation = value; OnPropertyChanged(); }
        }

        // Commands
        public RelayCommand SendMessageCommand { get; }
        public RelayCommand ResetConversationCommand { get; }
        public RelayCommand RefreshCommand { get; }

        // Methods
        private async Task InitializeAsync()
        {
            try
            {
                var isHealthy = await _apiClient.CheckHealthAsync();
                if (!isHealthy)
                {
                    ErrorMessage = "Assistant API is not available";
                    return;
                }

                _apiClient.StartStatusPolling(TimeSpan.FromSeconds(2));
                await RefreshDataAsync();
            }
            catch (Exception ex)
            {
                ErrorMessage = $"Initialization failed: {ex.Message}";
            }
        }

        private async Task SendMessageAsync()
        {
            if (string.IsNullOrWhiteSpace(CurrentMessage)) return;

            var message = CurrentMessage;
            CurrentMessage = "";
            IsLoading = true;
            ErrorMessage = "";

            try
            {
                await _apiClient.AskQuestionAsync(message);
                await RefreshConversationAsync();
            }
            catch (Exception ex)
            {
                ErrorMessage = $"Failed to send message: {ex.Message}";
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task ResetConversationAsync()
        {
            IsLoading = true;
            ErrorMessage = "";

            try
            {
                await _apiClient.ResetConversationAsync();
                Conversation = new List<ConversationEntry>();
            }
            catch (Exception ex)
            {
                ErrorMessage = $"Failed to reset conversation: {ex.Message}";
            }
            finally
            {
                IsLoading = false;
            }
        }

        private async Task RefreshDataAsync()
        {
            await RefreshConversationAsync();
        }

        private async Task RefreshConversationAsync()
        {
            try
            {
                var conversation = await _apiClient.GetConversationAsync();
                Conversation = conversation;
                ErrorMessage = "";
            }
            catch (Exception ex)
            {
                ErrorMessage = $"Failed to refresh conversation: {ex.Message}";
            }
        }

        private void OnStatusUpdated(object sender, AssistantStatus status)
        {
            Status = status;
            ErrorMessage = "";
        }

        private void OnErrorOccurred(object sender, string error)
        {
            ErrorMessage = $"Status error: {error}";
        }

        public void Dispose()
        {
            _apiClient?.Dispose();
        }

        // INotifyPropertyChanged
        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    // Simple RelayCommand implementation
    public class RelayCommand
    {
        private readonly Func<Task> _executeAsync;
        private readonly Func<bool> _canExecute;
        private bool _isExecuting;

        public RelayCommand(Func<Task> executeAsync, Func<bool> canExecute = null)
        {
            _executeAsync = executeAsync ?? throw new ArgumentNullException(nameof(executeAsync));
            _canExecute = canExecute;
        }

        public event EventHandler CanExecuteChanged;

        public bool CanExecute(object parameter)
        {
            return !_isExecuting && (_canExecute?.Invoke() ?? true);
        }

        public async void Execute(object parameter)
        {
            if (CanExecute(parameter))
            {
                try
                {
                    _isExecuting = true;
                    await _executeAsync();
                }
                finally
                {
                    _isExecuting = false;
                }
            }

            RaiseCanExecuteChanged();
        }

        public void RaiseCanExecuteChanged()
        {
            CanExecuteChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    // =============================================================================
    // CONSOLE APPLICATION EXAMPLE
    // =============================================================================

    public class ConsoleChatApp
    {
        private readonly AssistantApiClient _apiClient;

        public ConsoleChatApp(string apiUrl = "http://localhost:5001")
        {
            _apiClient = new AssistantApiClient(apiUrl);
        }

        public async Task RunAsync()
        {
            Console.WriteLine("AI Voice Assistant - C# Console Interface");
            Console.WriteLine("Type 'quit' to exit, 'status' for status, 'reset' to reset conversation");
            Console.WriteLine(new string('-', 60));

            // Check health
            if (!await _apiClient.CheckHealthAsync())
            {
                Console.WriteLine("ERROR: Assistant API is not available!");
                return;
            }

            // Show initial status
            try
            {
                var status = await _apiClient.GetStatusAsync();
                Console.WriteLine($"Connected to assistant. Questions asked: {status.QuestionCount}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Warning: Could not get status - {ex.Message}");
            }

            Console.WriteLine(new string('-', 60));

            // Chat loop
            while (true)
            {
                Console.Write("\nYou: ");
                var input = Console.ReadLine()?.Trim();

                if (string.IsNullOrEmpty(input)) continue;

                if (input.ToLower() is "quit" or "exit" or "q")
                    break;

                if (input.ToLower() == "status")
                {
                    await ShowStatusAsync();
                    continue;
                }

                if (input.ToLower() == "reset")
                {
                    await ResetConversationAsync();
                    continue;
                }

                // Ask question
                try
                {
                    Console.WriteLine("Assistant: Processing...");
                    var response = await _apiClient.AskQuestionAsync(input);
                    Console.WriteLine($"Assistant: {response.Answer}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                }
            }

            Console.WriteLine("\nGoodbye!");
        }

        private async Task ShowStatusAsync()
        {
            try
            {
                var status = await _apiClient.GetStatusAsync();
                var stats = await _apiClient.GetStatsAsync();

                Console.WriteLine("\n--- Assistant Status ---");
                Console.WriteLine($"Status: {status.AssistantStatusValue}");
                Console.WriteLine($"Questions asked: {status.QuestionCount}");
                Console.WriteLine($"Session ID: {status.SessionId}");
                Console.WriteLine($"Last question: {status.CurrentQuestion ?? "None"}");
                Console.WriteLine($"Last answer: {status.CurrentAnswer ?? "None"}");
                Console.WriteLine($"Total conversation entries: {stats.ConversationEntries}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error getting status: {ex.Message}");
            }
        }

        private async Task ResetConversationAsync()
        {
            try
            {
                var result = await _apiClient.ResetConversationAsync();
                Console.WriteLine($"Conversation reset. New session: {result.SessionId}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error resetting conversation: {ex.Message}");
            }
        }

        public void Dispose()
        {
            _apiClient?.Dispose();
        }
    }

    // =============================================================================
    // ASP.NET CORE CONTROLLER EXAMPLE
    // =============================================================================

    /* 
    // Add to your ASP.NET Core project

    [ApiController]
    [Route("api/[controller]")]
    public class AssistantProxyController : ControllerBase
    {
        private readonly AssistantApiClient _apiClient;

        public AssistantProxyController(AssistantApiClient apiClient)
        {
            _apiClient = apiClient;
        }

        [HttpGet("status")]
        public async Task<IActionResult> GetStatus()
        {
            try
            {
                var status = await _apiClient.GetStatusAsync();
                return Ok(status);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }

        [HttpPost("ask")]
        public async Task<IActionResult> AskQuestion([FromBody] AskQuestionRequest request)
        {
            try
            {
                var response = await _apiClient.AskQuestionAsync(request.Question, request.UserId);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }

        [HttpGet("conversation")]
        public async Task<IActionResult> GetConversation([FromQuery] string userId, [FromQuery] int? limit)
        {
            try
            {
                var conversation = await _apiClient.GetConversationAsync(userId, limit);
                return Ok(new { conversation });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }

        [HttpPost("reset")]
        public async Task<IActionResult> ResetConversation()
        {
            try
            {
                var result = await _apiClient.ResetConversationAsync();
                return Ok(result);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
    }

    public class AskQuestionRequest
    {
        public string Question { get; set; } = "";
        public string? UserId { get; set; }
    }

    // In Program.cs or Startup.cs:
    // builder.Services.AddSingleton<AssistantApiClient>();
    */

    // =============================================================================
    // USAGE EXAMPLES
    // =============================================================================

    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("AI Assistant C# Client Examples");
            Console.WriteLine("1. Simple API Example");
            Console.WriteLine("2. Interactive Chat");
            Console.WriteLine("3. Status Monitoring");
            
            Console.Write("Choose an option (1-3): ");
            var choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    await SimpleApiExample();
                    break;
                case "2":
                    await InteractiveChatExample();
                    break;
                case "3":
                    await StatusMonitoringExample();
                    break;
                default:
                    await InteractiveChatExample();
                    break;
            }
        }

        static async Task SimpleApiExample()
        {
            Console.WriteLine("\n=== Simple API Example ===");
            
            using var client = new AssistantApiClient();

            try
            {
                // Check health
                if (!await client.CheckHealthAsync())
                {
                    Console.WriteLine("Assistant API is not available!");
                    return;
                }

                // Get status
                var status = await client.GetStatusAsync();
                Console.WriteLine($"Status: {status.AssistantStatusValue}");
                Console.WriteLine($"Questions asked: {status.QuestionCount}");

                // Ask a question
                Console.WriteLine("\nAsking: 'What time is it?'");
                var response = await client.AskQuestionAsync("What time is it?");
                Console.WriteLine($"Answer: {response.Answer}");

                // Get conversation
                var conversation = await client.GetConversationAsync(limit: 5);
                Console.WriteLine($"\nConversation has {conversation.Count} entries");

                // Get example questions
                var examples = await client.GetExampleQuestionsAsync();
                Console.WriteLine($"\nExample questions available: {examples.Count}");
                for (int i = 0; i < Math.Min(3, examples.Count); i++)
                {
                    var example = examples[i];
                    Console.WriteLine($"  - {example.Question} ({example.Category})");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }

        static async Task InteractiveChatExample()
        {
            Console.WriteLine("\n=== Interactive Chat Example ===");
            
            var chatApp = new ConsoleChatApp();
            await chatApp.RunAsync();
            chatApp.Dispose();
        }

        static async Task StatusMonitoringExample()
        {
            Console.WriteLine("\n=== Status Monitoring Example ===");
            
            using var client = new AssistantApiClient();
            
            // Set up event handlers
            client.StatusUpdated += (sender, status) =>
            {
                Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Status: {status.AssistantStatusValue}, Questions: {status.QuestionCount}");
                if (!string.IsNullOrEmpty(status.CurrentQuestion))
                {
                    Console.WriteLine($"  Current Q: {status.CurrentQuestion}");
                    Console.WriteLine($"  Current A: {status.CurrentAnswer}");
                }
            };

            client.ErrorOccurred += (sender, error) =>
            {
                Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Error: {error}");
            };

            // Start monitoring
            client.StartStatusPolling(TimeSpan.FromSeconds(2));
            
            Console.WriteLine("Monitoring status... Press any key to stop.");
            Console.ReadKey();
            
            client.StopStatusPolling();
        }
    }
}
