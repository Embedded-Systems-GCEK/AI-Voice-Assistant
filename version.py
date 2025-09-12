#!/usr/bin/env python3
"""
Version management utility for AI Voice Assistant
"""

import os
import sys
import re
import json
from typing import Optional


def get_version() -> str:
    """Get current version from VERSION file"""
    try:
        with open("VERSION", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"


def set_version(new_version: str) -> bool:
    """Set new version in VERSION file"""
    # Validate version format (basic semver)
    if not re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$', new_version):
        print(f"Error: Invalid version format '{new_version}'. Expected format: X.Y.Z or X.Y.Z-suffix")
        return False
    
    try:
        with open("VERSION", "w") as f:
            f.write(new_version)
        print(f"✅ Version updated to {new_version}")
        return True
    except Exception as e:
        print(f"Error updating version: {e}")
        return False


def get_release_info() -> dict:
    """Get release information"""
    version = get_version()
    
    # Check if we're in a git repository
    try:
        import subprocess
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], 
            stderr=subprocess.DEVNULL
        ).decode().strip()
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            stderr=subprocess.DEVNULL  
        ).decode().strip()
    except:
        commit = "unknown"
        branch = "unknown"
    
    return {
        "version": version,
        "commit": commit,
        "branch": branch,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    }


def main():
    if len(sys.argv) < 2:
        print("AI Voice Assistant Version Manager")
        print("=" * 40)
        
        info = get_release_info()
        print(f"Current Version: {info['version']}")
        print(f"Git Commit: {info['commit']}")
        print(f"Git Branch: {info['branch']}")
        print(f"Python Version: {info['python_version']}")
        
        print("\nUsage:")
        print("  python version.py get                 # Show current version")
        print("  python version.py set <version>       # Set new version")
        print("  python version.py info                # Show release info")
        return
    
    command = sys.argv[1].lower()
    
    if command == "get":
        print(get_version())
    
    elif command == "set":
        if len(sys.argv) < 3:
            print("Error: Version not specified")
            print("Usage: python version.py set <version>")
            sys.exit(1)
        
        new_version = sys.argv[2]
        if not set_version(new_version):
            sys.exit(1)
    
    elif command == "info":
        info = get_release_info()
        print(json.dumps(info, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: get, set, info")
        sys.exit(1)


if __name__ == "__main__":
    main()