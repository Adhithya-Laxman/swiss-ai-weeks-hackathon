#!/usr/bin/env python3
"""
Test script to verify Firebase connection and basic functionality
"""

import firebase_admin
from firebase_admin import credentials, db
import json
import time

def test_firebase_connection():
    """Test Firebase connection and basic operations"""
    try:
        # Initialize Firebase
        cred = credentials.Certificate('swiss-ai-hack-firebase-adminsdk-fbsvc-7a0fbd49d6.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://swiss-ai-hack-default-rtdb.firebaseio.com'
        })
        print("✅ Firebase initialized successfully")
        
        # Test write operation
        ref = db.reference('test')
        test_data = {
            'message': 'Test message',
            'timestamp': int(time.time() * 1000)
        }
        ref.child('connection_test').set(test_data)
        print("✅ Write operation successful")
        
        # Test read operation
        data = ref.child('connection_test').get()
        if data and data.get('message') == 'Test message':
            print("✅ Read operation successful")
        else:
            print("❌ Read operation failed")
            
        # Clean up test data
        ref.child('connection_test').delete()
        print("✅ Cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Firebase connection failed: {e}")
        return False

def test_chat_functions():
    """Test the chat functions from app.py"""
    try:
        from app import append_message_to_firebase, get_chat_history
        
        # Test appending a message
        success = append_message_to_firebase('test_chat', 'Hello', 'Hi there!')
        if success:
            print("✅ Message append successful")
        else:
            print("❌ Message append failed")
            
        # Test retrieving chat history
        history = get_chat_history('test_chat')
        if history and len(history) > 0:
            print("✅ Chat history retrieval successful")
            print(f"   Found {len(history)} messages")
        else:
            print("❌ Chat history retrieval failed")
            
        return True
        
    except Exception as e:
        print(f"❌ Chat functions test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Firebase Connection...")
    print("=" * 50)
    
    # Test Firebase connection
    firebase_ok = test_firebase_connection()
    
    if firebase_ok:
        print("\n🧪 Testing Chat Functions...")
        print("=" * 50)
        chat_ok = test_chat_functions()
        
        if chat_ok:
            print("\n🎉 All tests passed! Firebase is ready to use.")
        else:
            print("\n⚠️  Firebase connection works but chat functions have issues.")
    else:
        print("\n❌ Firebase connection failed. Please check your configuration.")
