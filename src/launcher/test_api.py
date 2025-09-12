import time
import requests
import json



def test_api_endpoints(host: str = "localhost", port: int = 5001):
    """Test the API endpoints with sample requests"""
    
    base_url = f"http://{host}:{port}"
    
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

