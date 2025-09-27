#!/usr/bin/env python3
"""
Test script to verify chat functionality
"""

import requests
import json
import time

def test_chat_api():
    """Test the chat API endpoint"""
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Chat API...")
    print("=" * 50)
    
    # Test data
    test_message = "Hello, can you help me with disaster management?"
    chat_id = "test_chat_" + str(int(time.time()))
    
    try:
        # Test the chat endpoint
        response = requests.post(
            f"{base_url}/chat",
            json={
                "message": test_message,
                "chat_id": chat_id
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('error'):
                print(f"❌ API returned error: {data.get('response')}")
                return False
            else:
                print("✅ Chat API working!")
                print(f"   User: {test_message}")
                print(f"   AI: {data.get('response', 'No response')[:100]}...")
                return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error testing chat API: {e}")
        return False

def test_home_page():
    """Test the home page"""
    base_url = "http://localhost:5001"
    
    print("\n🧪 Testing Home Page...")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Home page accessible")
            return True
        else:
            print(f"❌ Home page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing home page: {e}")
        return False

def test_chatbot_page():
    """Test the chatbot page"""
    base_url = "http://localhost:5001"
    
    print("\n🧪 Testing Chatbot Page...")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}/chatbot", timeout=10)
        if response.status_code == 200:
            print("✅ Chatbot page accessible")
            return True
        else:
            print(f"❌ Chatbot page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing chatbot page: {e}")
        return False

if __name__ == "__main__":
    print("🚨 Testing Disaster Management Chatbot")
    print("=" * 50)
    
    # Test pages
    home_ok = test_home_page()
    chatbot_ok = test_chatbot_page()
    
    # Test chat API (only if pages work)
    if home_ok and chatbot_ok:
        chat_ok = test_chat_api()
        
        if chat_ok:
            print("\n🎉 All tests passed! The chatbot is working correctly.")
        else:
            print("\n⚠️  Pages work but chat API has issues.")
    else:
        print("\n❌ Basic pages are not accessible. Check if the server is running.")
    
    print("\n🌐 You can now access:")
    print("   Home: http://localhost:5001")
    print("   Chatbot: http://localhost:5001/chatbot")
