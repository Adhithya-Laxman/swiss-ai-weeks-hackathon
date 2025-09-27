#!/usr/bin/env python3
"""
Simple script to create .env file with API key
"""

def create_env_file():
    """Create .env file with API key"""
    print("🚨 Swisscom Apertus API Setup")
    print("=" * 50)
    print("This script will create a .env file with your API key.")
    print("You can also manually create a .env file with:")
    print("SWISSCOM_API=your_api_key_here")
    print()
    
    api_key = "rcShIW6CWHQS5NO9AOmTqJSwKvCN"
    
    if not api_key:
        print("❌ No API key provided. Exiting.")
        return
    
    # Create .env file
    env_content = f"# Swisscom Apertus API Configuration\nSWISSCOM_API={api_key}\n"
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print(f"✅ .env file created successfully with API key: {api_key[:10]}...")
        print("✅ You can now run the app with: python run_app.py")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("You can manually create a .env file with:")
        print(f"SWISSCOM_API={api_key}")

if __name__ == "__main__":
    create_env_file()
