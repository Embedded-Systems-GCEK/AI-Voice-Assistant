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
    print(f"{color_code}[STARTUP] Starting {name} on port {port}...{color_code}")
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
        
        print(f"{color_code}[SUCCESS] {name} started with PID {process.pid}{color_code}")
        
        # Print output in real-time
        if process.stdout:
            for line in process.stdout:
                print(f"{color_code}[{name}] {line.rstrip()}{color_code}")
            
        process.wait()
        print(f"{color_code}[STOPPED] {name} stopped{color_code}")
        
    except Exception as e:
        print(f"{color_code}[ERROR] Failed to start {name}: {e}{color_code}")

def start_all_servers():
    """Start all servers concurrently"""
    
    print("=" * 60)
    print("[STARTUP] AI VOICE ASSISTANT - MULTI-SERVER LAUNCHER")
    print("=" * 60)
    print()
    
    servers = [
        {
            "name": "API Server",
            "command": f"{sys.executable} api_server.py",
            "port": 5001,
            "color": ""  # No color codes to avoid issues
        },
        {
            "name": "Unified Server", 
            "command": f"{sys.executable} server/server.py",
            "port": 5000,
            "color": ""
        }
    ]
    
    print("[INFO] Server Configuration:")
    for server in servers:
        print(f"   • {server['name']:<15} → http://localhost:{server['port']}")
    print()
    
    print("[INFO] Flutter Integration Endpoints:")
    print("   • Main API:      http://localhost:5001/api/")
    print("   • Server API:    http://localhost:5000/api/")
    print()
    
    print("[INFO] Flutter App Usage:")
    print("   • Use http://localhost:5001 as your base URL for Flutter apps")
    print("   • Use http://localhost:5000 for web UI and general API access")
    print("   • Available endpoints:")
    print("     - GET  /api/status           → Assistant status & current Q&A")
    print("     - POST /api/ask              → Ask questions")
    print("     - GET  /api/conversation     → Get conversation history")
    print("     - GET  /api/stats            → Get statistics")
    print("     - GET  /api/example-questions → Get example questions")
    print("     - POST /api/reset            → Reset conversation")
    print()
    
    print("[STARTUP] Starting servers (this may take a moment)...")
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
            print("\n[INFO] All servers are starting...")
            print("[INFO] Press Ctrl+C to stop all servers")
            print("-" * 60)
            
            # Wait for all servers
            for future in futures:
                future.result()
                
        except KeyboardInterrupt:
            print("\n\n[SHUTDOWN] Shutting down all servers...")
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


    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            test_api_endpoints()
        elif sys.argv[1] == '--guide':
          pass
            # how_flutter_integration_guide()s
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
