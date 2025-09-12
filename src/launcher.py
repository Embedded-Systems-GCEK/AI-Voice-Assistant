#!/usr/bin/env python3
"""
Multi-Server Launcher for AI Voice Assistant
Starts all necessary servers for complete Flutter integration
"""

import subprocess
import threading
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor
import webbrowser

# Custom imports

from launcher.test_api import test_api_endpoints
from launcher.start_all_server import start_all_servers


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--run':
          start_all_servers()
        elif sys.argv[1] == '--test':
          test_api_endpoints()
        elif sys.argv[1] == '--guide':
          pass
            
        else:
            print("Usage:")
            print("  python launcher.py --run  # Start all servers")
            print("  python launcher.py --test # Test API endpoints")
    else:
        try:
            start_all_servers()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
