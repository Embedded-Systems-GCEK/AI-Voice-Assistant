
import subprocess
import threading
import os
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

    
