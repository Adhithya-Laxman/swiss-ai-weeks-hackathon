#!/usr/bin/env python3
"""
Startup script for the Disaster Management Chatbot
"""

import os
import sys
from app import app

def check_environment():
    """Check if required environment variables are set"""
    if not os.getenv("SWISSCOM_API"):
        print("⚠️  Warning: SWISSCOM_API environment variable not set")
        print("   Set it with: export SWISSCOM_API='your_api_key_here'")
        print("   The app will still run but API calls may fail")
        return False
    return True

def check_firebase_credentials():
    """Check if Firebase credentials file exists"""
    if not os.path.exists('swiss-ai-hack-firebase-adminsdk-fbsvc-7a0fbd49d6.json'):
        print("❌ Error: Firebase credentials file not found")
        print("   Please ensure 'swiss-ai-hack-firebase-adminsdk-fbsvc-7a0fbd49d6.json' is in the current directory")
        return False
    return True

def main():
    """Main startup function"""
    print("🚨 Starting Disaster Management Chatbot...")
    print("=" * 50)
    
    # Check environment
    env_ok = check_environment()
    firebase_ok = check_firebase_credentials()
    
    if not firebase_ok:
        print("\n❌ Cannot start application due to missing Firebase credentials")
        sys.exit(1)
    
    if not env_ok:
        print("\n⚠️  Starting with warnings...")
    
    print("\n🌐 Application will be available at:")
    print("   Home: http://localhost:5001")
    print("   Chatbot: http://localhost:5001/chatbot")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the Flask app
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
