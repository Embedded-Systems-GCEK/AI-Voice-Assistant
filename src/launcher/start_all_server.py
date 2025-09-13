

import sys
import time
from concurrent.futures import ThreadPoolExecutor

# Custom imports
from launcher.run_server import run_server

def start_all_servers():
    """Start all servers concurrently"""
    print("=" * 60)
    print("[STARTUP] AI VOICE ASSISTANT - MULTI-SERVER LAUNCHER")
    print("=" * 60)
    print()
    
    servers = [
        {
            "name": "API Server",
            "command": f"{sys.executable} ../api_server.py",
            "port": 5001,
            "color": ""  # No color codes to avoid issues
        },
        {
            "name": "Unified Server", 
            "command": f"{sys.executable} ../server/server.py",
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
            print(server["command"] , "Server Command")
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
