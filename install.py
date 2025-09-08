#!/usr/bin/env python3
"""
AI Voice Assistant Installation and Setup Script
This script helps install and set up the voice assistant on different platforms
"""

import sys
import os
import subprocess
import platform
import urllib.request
import json
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a numbered step"""
    print(f"\n{step}. {description}")

def run_command(cmd, description, ignore_errors=False):
    """Run a shell command and return success status"""
    print(f"   Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"   ⚠️  {description} - Warning: {e}")
            return False
        else:
            print(f"   ❌ {description} - Failed: {e}")
            return False
    except Exception as e:
        print(f"   ❌ {description} - Error: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported")
        print("   Please install Python 3.7 or later")
        return False

def setup_virtual_environment():
    """Create and setup virtual environment"""
    print_step(1, "Setting up virtual environment")
    
    if not run_command([sys.executable, "-m", "venv", ".venv"], "Create virtual environment"):
        return False
    
    # Determine activation script path based on platform
    if platform.system() == "Windows":
        activate_script = os.path.join(".venv", "Scripts", "activate")
        pip_path = os.path.join(".venv", "Scripts", "pip")
    else:
        activate_script = os.path.join(".venv", "bin", "activate")
        pip_path = os.path.join(".venv", "bin", "pip")
    
    print(f"   Virtual environment created at: .venv")
    print(f"   To activate manually:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    
    return True, pip_path

def install_packages(pip_path):
    """Install required packages"""
    print_step(2, "Installing Python packages")
    
    # Try to upgrade pip first
    run_command([pip_path, "install", "--upgrade", "pip"], "Upgrade pip", ignore_errors=True)
    
    # Install packages individually for better error handling
    packages = [
        "speechrecognition",
        "cohere",
        "requests"
    ]
    
    success = True
    for package in packages:
        if not run_command([pip_path, "install", package], f"Install {package}", ignore_errors=True):
            print(f"   ⚠️  Could not install {package} - continuing anyway")
            success = False
    
    # PyAudio often needs special handling
    print("\n   Installing PyAudio (may require system libraries)...")
    if platform.system() == "Linux":
        print("   You may need to install system packages:")
        print("   sudo apt-get install portaudio19-dev python3-pyaudio")
    elif platform.system() == "Darwin":  # macOS
        print("   You may need to install system packages:")
        print("   brew install portaudio")
    
    run_command([pip_path, "install", "pyaudio"], "Install PyAudio", ignore_errors=True)
    
    return success

def download_piper_tts():
    """Download Piper TTS for the current platform"""
    print_step(3, "Setting up Piper TTS")
    
    piper_dir = Path("piper")
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Map system and architecture to Piper release names
    if system == "linux":
        if "x86_64" in machine or "amd64" in machine:
            piper_release = "piper_linux_x86_64.tar.gz"
            piper_exe = "piper"
        elif "aarch64" in machine or "arm64" in machine:
            piper_release = "piper_linux_aarch64.tar.gz" 
            piper_exe = "piper"
        else:
            print(f"   ⚠️  Unsupported Linux architecture: {machine}")
            return False
    elif system == "darwin":  # macOS
        piper_release = "piper_macos_x64.tar.gz"
        piper_exe = "piper"
    elif system == "windows":
        piper_release = "piper_windows_amd64.zip"
        piper_exe = "piper.exe"
    else:
        print(f"   ⚠️  Unsupported operating system: {system}")
        return False
    
    # Check if we already have the right executable
    target_exe = piper_dir / piper_exe
    if target_exe.exists():
        print(f"   ✅ Piper executable already exists: {target_exe}")
        return True
    
    # Check if we have Windows executable on Linux (common issue)
    windows_exe = piper_dir / "piper.exe"
    if windows_exe.exists() and system != "windows":
        print(f"   ⚠️  Found Windows Piper executable but running on {system}")
        print(f"   Downloading {system} version...")
    
    print(f"   Downloading Piper TTS for {system} {machine}...")
    print(f"   This may take a while...")
    
    # For now, just provide download instructions since we can't easily download and extract
    print(f"   Please manually download Piper TTS:")
    print(f"   1. Go to: https://github.com/rhasspy/piper/releases")
    print(f"   2. Download: {piper_release}")
    print(f"   3. Extract to the piper/ directory")
    print(f"   4. Ensure the executable is named: {piper_exe}")
    
    return False

def setup_configuration():
    """Setup configuration files"""
    print_step(4, "Configuring the voice assistant")
    
    # Check dictionaries.json
    if os.path.exists("dictionaries.json"):
        print("   ✅ dictionaries.json already exists")
    else:
        print("   ⚠️  dictionaries.json not found")
        return False
    
    # Check source files
    src_files = ["app.py", "assistant.py", "cohere_api.py", "files.py", "ollama.py", "status.py", "tts.py"]
    missing_files = []
    
    for filename in src_files:
        if os.path.exists(os.path.join("src", filename)):
            print(f"   ✅ src/{filename}")
        else:
            print(f"   ❌ src/{filename} is missing")
            missing_files.append(filename)
    
    if missing_files:
        print(f"   ❌ Missing source files: {missing_files}")
        return False
    
    # Check Cohere API configuration
    cohere_file = os.path.join("src", "cohere_api.py")
    try:
        with open(cohere_file, 'r') as f:
            content = f.read()
            if 'COHERE_API_KEY = ""' in content or 'your_api_key_here' in content:
                print("   ⚠️  Cohere API key not configured")
                print("   Edit src/cohere_api.py to add your API key from https://cohere.com")
            else:
                print("   ✅ Cohere API key is configured")
    except Exception as e:
        print(f"   ⚠️  Could not check Cohere configuration: {e}")
    
    return True

def create_run_script():
    """Create a run script for easy startup"""
    print_step(5, "Creating run script")
    
    if platform.system() == "Windows":
        script_content = """@echo off
echo Starting AI Voice Assistant...
call .venv\\Scripts\\activate
python src\\app.py
pause
"""
        script_name = "run_assistant.bat"
    else:
        script_content = """#!/bin/bash
echo "Starting AI Voice Assistant..."
source .venv/bin/activate
python src/app.py
"""
        script_name = "run_assistant.sh"
    
    try:
        with open(script_name, 'w') as f:
            f.write(script_content)
        
        if platform.system() != "Windows":
            os.chmod(script_name, 0o755)  # Make executable
        
        print(f"   ✅ Created {script_name}")
        print(f"   You can now run the assistant with: ./{script_name}")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create run script: {e}")
        return False

def print_final_instructions():
    """Print final setup instructions"""
    print_header("Setup Complete!")
    
    print("\n📋 Next Steps:")
    print("1. If Piper TTS download failed, manually download it:")
    print("   https://github.com/rhasspy/piper/releases")
    print("   Extract to the piper/ directory")
    
    print("\n2. (Optional) Configure Cohere API:")
    print("   - Get a free API key from https://cohere.com")
    print("   - Edit src/cohere_api.py and add your key")
    
    print("\n3. (Optional) Install Ollama for offline AI:")
    print("   - Visit https://ollama.ai/")
    print("   - Install Ollama")
    print("   - Run: ollama run mistral:7b")
    
    print("\n4. Run the voice assistant:")
    if platform.system() == "Windows":
        print("   run_assistant.bat")
    else:
        print("   ./run_assistant.sh")
    print("   or manually:")
    if platform.system() == "Windows":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("   python src/app.py")
    
    print("\n5. Test the setup:")
    print("   python test_setup.py")

def main():
    """Main installation function"""
    print_header("AI Voice Assistant Installation")
    print(f"Platform: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    
    if not check_python_version():
        sys.exit(1)
    
    # Change to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    # Setup steps
    success = True
    
    # Step 1: Virtual environment
    result = setup_virtual_environment()
    if isinstance(result, tuple):
        success &= result[0]
        pip_path = result[1]
    else:
        success &= result
        pip_path = "pip"
    
    # Step 2: Install packages
    if success:
        success &= install_packages(pip_path)
    
    # Step 3: Piper TTS
    success &= download_piper_tts()
    
    # Step 4: Configuration
    success &= setup_configuration()
    
    # Step 5: Run script
    success &= create_run_script()
    
    # Final instructions
    print_final_instructions()
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("Run 'python test_setup.py' to verify your setup.")
    else:
        print("\n⚠️  Installation completed with some issues.")
        print("Please address the warnings above and run 'python test_setup.py' to verify.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())