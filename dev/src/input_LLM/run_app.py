#!/usr/bin/env python3
"""
DisasterAI Application Runner
This script starts the Flask application with proper configuration
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5002))
    
    print("🚨 Starting Disaster Management Chatbot...")
    print("=" * 50)
    print("🌐 Application will be available at:")
    print(f"   Home: http://localhost:{port}")
    print(f"   Chatbot: http://localhost:{port}/chatbot")
    print(f"   Game: http://localhost:{port}/game")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
