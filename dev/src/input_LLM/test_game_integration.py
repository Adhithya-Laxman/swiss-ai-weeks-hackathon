#!/usr/bin/env python3
"""
Test script for the complete game-chatbot integration
"""

import requests
import json
import time

def test_complete_flow():
    """Test the complete game-to-chatbot flow"""
    base_url = "http://localhost:5001"
    
    print("🎮 Testing Mario's Disaster Management Adventure Integration")
    print("=" * 70)
    
    # Test 1: Home page
    print("\n1. Testing Home Page...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Home page accessible")
        else:
            print(f"❌ Home page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing home page: {e}")
        return False
    
    # Test 2: Game page
    print("\n2. Testing Game Page...")
    try:
        response = requests.get(f"{base_url}/game", timeout=10)
        if response.status_code == 200:
            print("✅ Game page accessible")
        else:
            print(f"❌ Game page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing game page: {e}")
        return False
    
    # Test 3: Game-chatbot integration with different disasters
    print("\n3. Testing Game-Chatbot Integration...")
    
    disasters = [
        {
            "name": "Bolivia Wildfires",
            "title": "Bolivia Wildfires: Relief Phase Initiated",
            "context": "National emergency declared, requesting international support"
        },
        {
            "name": "Afghanistan Earthquake", 
            "title": "Earthquake in Nangarhar Province, Afghanistan",
            "context": "6+ magnitude earthquake with severe humanitarian impact"
        },
        {
            "name": "Yemen Flooding",
            "title": "Southern Yemen Flooding - Response Overview", 
            "context": "Severe flooding affecting 100,000 people"
        },
        {
            "name": "Congo Ebola",
            "title": "Ebola Outbreak in Democratic Republic of Congo",
            "context": "Health authorities declared outbreak in Kasai Province"
        }
    ]
    
    for i, disaster in enumerate(disasters, 1):
        print(f"\n   Testing {disaster['name']}...")
        try:
            url = f"{base_url}/game-chatbot?disaster={disaster['title']}&context={disaster['context']}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {disaster['name']} integration working")
            else:
                print(f"   ❌ {disaster['name']} error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {disaster['name']} error: {e}")
    
    # Test 4: Chat API with game context
    print("\n4. Testing Chat API with Game Context...")
    try:
        response = requests.post(
            f"{base_url}/chat",
            json={
                "message": "What are the immediate relief needs for this disaster?",
                "chat_id": "game_test_chat"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('error'):
                print(f"❌ Chat API error: {data.get('response')}")
            else:
                print("✅ Chat API working with game context")
                print(f"   AI Response: {data.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Chat API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat API error: {e}")
    
    # Test 5: Regular chatbot
    print("\n5. Testing Regular Chatbot...")
    try:
        response = requests.get(f"{base_url}/chatbot", timeout=10)
        if response.status_code == 200:
            print("✅ Regular chatbot accessible")
        else:
            print(f"❌ Regular chatbot error: {response.status_code}")
    except Exception as e:
        print(f"❌ Regular chatbot error: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 INTEGRATION TEST COMPLETE!")
    print("\n🌐 Available URLs:")
    print(f"   Home: {base_url}/")
    print(f"   Game: {base_url}/game")
    print(f"   Chatbot: {base_url}/chatbot")
    print(f"   Game-Chatbot: {base_url}/game-chatbot")
    
    print("\n🎮 Game Flow:")
    print("   1. Start at home page")
    print("   2. Click 'Play Mario's Disaster Adventure'")
    print("   3. Click START in the game")
    print("   4. Click on disaster emoji locations (🔥🪨🌧️🦟)")
    print("   5. Click 'Continue to Disaster Management'")
    print("   6. Get AI assistance with disaster context")
    print("   7. Click 'Back to Mario's Adventure' to return to game")
    
    return True

if __name__ == "__main__":
    test_complete_flow()
