#!/usr/bin/env python3
"""
Setup script to help configure the Swisscom API key
"""

import os
import sys

def setup_api_key():
    """Interactive setup for the Swisscom API key"""
    print("🚨 Swisscom Apertus API Setup")
    print("=" * 50)
    
    # Check if API key is already set
    current_key = os.getenv("SWISSCOM_API")
    if current_key:
        print(f"✅ SWISSCOM_API is already set: {current_key[:10]}...")
        choice = input("Do you want to update it? (y/n): ").lower().strip()
        if choice != 'y':
            print("Keeping existing API key.")
            return
    
    print("\nTo use the Apertus AI model, you need a Swisscom API key.")
    print("Please enter your Swisscom API key:")
    
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    # Set the environment variable for current session
    os.environ["SWISSCOM_API"] = api_key
    
    print(f"\n✅ API key set for current session: {api_key[:10]}...")
    
    # Provide instructions for permanent setup
    print("\n📝 To make this permanent, add this to your shell profile:")
    print(f'   export SWISSCOM_API="{api_key}"')
    print("\n   Or create a .env file in this directory with:")
    print(f'   SWISSCOM_API="{api_key}"')
    
    # Test the API key
    print("\n🧪 Testing API key...")
    try:
        from app import client
        if client is not None:
            print("✅ API key is valid and client initialized successfully!")
        else:
            print("❌ API key validation failed.")
    except Exception as e:
        print(f"❌ Error testing API key: {e}")

if __name__ == "__main__":
    setup_api_key()
