#!/usr/bin/env python3
"""
Test script for the timeout functionality in the Assistant class.
This demonstrates how the 10-second timeout works and prompts for user information.
"""

import sys
import os

from src.assistant.assistant import ConversationalAssistant
from src.assistant.status.status import Status
from src.assistant.robot.answer_helper.tts.tts import PIPER_TTS
from src.assistant.ai_providers.ollama import Ollama
from src.assistant.files.files import Files

def test_timeout_assistant():
    """Test the assistant with timeout functionality"""
    print("=== AI Voice Assistant with Timeout Test ===")
    print("The assistant will wait for 10 seconds for your input.")
    print("If no input is received, it will ask prompting questions.")
    print("Press Ctrl+C to exit.\n")
    
    # Initialize required components
    status = Status()
    tts = PIPER_TTS()
    ollama = Ollama()
    files = Files()
    
    # Create assistant with timeout functionality
    assistant = ConversationalAssistant(
        name="ARIA",
        voice_config=None,
        status=status,
        tts=tts,
        ollama=ollama,
        files=files
    )
    
    # Set timeout to 10 seconds (you can change this)
    assistant.set_timeout(10)
    
    # Display initial conversation info
    info = assistant.get_conversation_info()
    print(f"Assistant Name: {info['assistant_name']}")
    print(f"Timeout: {info['timeout_seconds']} seconds")
    print(f"Connection Status: {'Online' if info['is_connected'] else 'Offline'}")
    print("-" * 50)
    
    # Greet the user
    assistant.greet()
    
    # Start the conversation loop with timeout
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        assistant.speak("Thank you for using the AI Assistant!")

def test_manual_commands():
    """Test specific timeout scenarios manually"""
    print("=== Manual Command Test ===")
    
    # Initialize components
    status = Status()
    tts = PIPER_TTS()
    ollama = Ollama()
    files = Files()
    
    assistant = ConversationalAssistant(
        name="ARIA",
        voice_config=None,
        status=status,
        tts=tts,
        ollama=ollama,
        files=files
    )
    assistant.set_timeout(5)  # Shorter timeout for testing
    
    print("Testing timeout scenarios:")
    print("1. Testing name extraction...")
    assistant.process_command("my name is john")
    
    print("\n2. Testing conversation info...")
    info = assistant.get_conversation_info()
    print(f"User Name: {info['user_name']}")
    print(f"State: {info['conversation_state']}")
    
    print("\n3. Testing prompt system...")
    assistant.ask_next_prompt()
    
    print("\n4. Testing reset...")
    assistant.reset_conversation()

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Full timeout test (interactive)")
    print("2. Manual command test (no audio)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_timeout_assistant()
    elif choice == "2":
        test_manual_commands()
    else:
        print("Invalid choice. Running manual test...")
        test_manual_commands()
