#!/usr/bin/env python3
"""
Test script to verify AI Voice Assistant setup
This script checks if all required components are available
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need Python 3.7+")
        return False

def check_package(package_name, required=True):
    """Check if a Python package is installed"""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            print(f"✅ {package_name} is installed")
            return True
        else:
            if required:
                print(f"❌ {package_name} is missing (required)")
            else:
                print(f"⚠️  {package_name} is missing (optional)")
            return False
    except ImportError:
        if required:
            print(f"❌ {package_name} is missing (required)")
        else:
            print(f"⚠️  {package_name} is missing (optional)")
        return False

def check_piper_tts():
    """Check if Piper TTS is available"""
    print("\n🎤 Checking Piper TTS setup...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    piper_dir = os.path.join(base_dir, "piper")
    
    # Check for both Windows and Linux executables
    piper_exe_win = os.path.join(piper_dir, "piper.exe")
    piper_exe_linux = os.path.join(piper_dir, "piper")
    
    model_file = os.path.join(piper_dir, "en_US-amy-low.onnx")
    config_file = os.path.join(piper_dir, "en_US-amy-low.onnx.json")
    
    # Determine which executable to use
    if sys.platform == "win32" and os.path.exists(piper_exe_win):
        piper_exe = piper_exe_win
        print(f"✅ Piper executable found: {piper_exe}")
    elif sys.platform != "win32" and os.path.exists(piper_exe_linux):
        piper_exe = piper_exe_linux
        print(f"✅ Piper executable found: {piper_exe}")
    elif os.path.exists(piper_exe_win):
        print(f"⚠️  Windows Piper executable found but running on {sys.platform}")
        print("   You may need to download the Linux version of Piper")
        print("   from: https://github.com/rhasspy/piper/releases")
        return False
    else:
        print(f"❌ Piper executable not found for {sys.platform}")
        print("   Download from: https://github.com/rhasspy/piper/releases")
        return False
    
    if os.path.exists(model_file):
        print(f"✅ Piper model found: {model_file}")
    else:
        print(f"❌ Piper model not found: {model_file}")
        return False
    
    if os.path.exists(config_file):
        print(f"✅ Piper config found: {config_file}")
    else:
        print(f"❌ Piper config not found: {config_file}")
        return False
        
    # Test Piper (only if executable is for current platform)
    try:
        result = subprocess.run(
            [piper_exe, "--help"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Piper TTS is working correctly")
            return True
        else:
            print(f"❌ Piper TTS test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Piper TTS test failed with error: {e}")
        return False

def check_dictionaries():
    """Check if dictionaries.json exists and is valid"""
    print("\n📚 Checking dictionaries.json...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dict_file = os.path.join(base_dir, "dictionaries.json")
    
    if not os.path.exists(dict_file):
        print(f"❌ dictionaries.json not found at: {dict_file}")
        return False
        
    try:
        import json
        with open(dict_file, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and len(data) > 0:
            print(f"✅ dictionaries.json is valid with {len(data)} entries")
            return True
        else:
            print("❌ dictionaries.json is empty or invalid")
            return False
    except Exception as e:
        print(f"❌ dictionaries.json is invalid: {e}")
        return False

def check_source_files():
    """Check if all required source files exist"""
    print("\n📁 Checking source files...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, "src")
    
    required_files = [
        "app.py",
        "assistant.py", 
        "cohere_api.py",
        "files.py",
        "ollama.py",
        "status.py",
        "tts.py"
    ]
    
    all_present = True
    for filename in required_files:
        filepath = os.path.join(src_dir, filename)
        if os.path.exists(filepath):
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} is missing")
            all_present = False
            
    return all_present

def main():
    """Main test function"""
    print("🚀 AI Voice Assistant Setup Verification")
    print("=" * 50)
    
    all_good = True
    
    # Check Python version
    all_good &= check_python_version()
    
    # Check required packages
    print("\n📦 Checking Python packages...")
    required_packages = [
        "json",      # built-in
        "os",        # built-in  
        "datetime",  # built-in
        "re",        # built-in
        "threading", # built-in
        "subprocess", # built-in
        "urllib",    # built-in
    ]
    
    optional_packages = [
        "speech_recognition",
        "pyaudio", 
        "cohere",
        "requests"
    ]
    
    for package in required_packages:
        all_good &= check_package(package, required=True)
        
    for package in optional_packages:
        check_package(package, required=False)
    
    # Check TTS setup
    all_good &= check_piper_tts()
    
    # Check dictionaries
    all_good &= check_dictionaries()
    
    # Check source files
    all_good &= check_source_files()
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Setup verification PASSED! The voice assistant should work.")
        print("\nTo run the assistant:")
        print("python src/app.py")
    else:
        print("⚠️  Setup verification found issues. Please fix them before running.")
        print("\nTo install missing packages:")
        print("pip install -r requirements.txt")
        
    return all_good

if __name__ == "__main__":
    main()