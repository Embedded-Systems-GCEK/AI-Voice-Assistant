#!/usr/bin/env python3
"""
Test script for the AI Assistant API with SQLAlchemy
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    print("Testing AI Assistant API with SQLAlchemy...")
    
    # Test health check
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    
    # Test root endpoint
    print("\n2. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.text}")
    
    # Test creating a user
    print("\n3. Testing user creation...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Create user: {response.status_code}")
    if response.status_code == 201:
        user = response.json()["user"]
        user_id = user["id"]
        print(f"Created user ID: {user_id}")
        
        # Test getting all users
        print("\n4. Testing get all users...")
        response = requests.get(f"{BASE_URL}/users")
        print(f"Get users: {response.status_code}")
        if response.status_code == 200:
            users = response.json()["users"]
            print(f"Total users: {len(users)}")
        
        # Test getting specific user
        print("\n5. Testing get specific user...")
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"Get user: {response.status_code}")
        
        # Test creating a question response
        print("\n6. Testing question response creation...")
        question_data = {
            "user_id": user_id,
            "question": "What is artificial intelligence?",
            "response": "Artificial intelligence (AI) is the simulation of human intelligence in machines.",
            "confidence_score": 0.95,
            "response_time_ms": 250
        }
        response = requests.post(f"{BASE_URL}/questions", json=question_data)
        print(f"Create question: {response.status_code}")
        if response.status_code == 201:
            question_response = response.json()["response"]
            response_id = question_response["id"]
            print(f"Created response ID: {response_id}")
            
            # Test getting user's questions
            print("\n7. Testing get user questions...")
            response = requests.get(f"{BASE_URL}/users/{user_id}/questions")
            print(f"Get user questions: {response.status_code}")
            
            # Test getting all question responses
            print("\n8. Testing get all question responses...")
            response = requests.get(f"{BASE_URL}/questions")
            print(f"Get all questions: {response.status_code}")
            
            # Test getting stats
            print("\n9. Testing stats endpoint...")
            response = requests.get(f"{BASE_URL}/stats")
            print(f"Get stats: {response.status_code}")
            if response.status_code == 200:
                stats = response.json()
                print(f"Stats: {json.dumps(stats, indent=2)}")
    
    print("\nAPI testing completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the server is running on http://localhost:5000")
    except Exception as e:
        print(f"Error: {e}")
