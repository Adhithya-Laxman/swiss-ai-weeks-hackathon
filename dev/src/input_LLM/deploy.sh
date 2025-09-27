#!/bin/bash

# DisasterAI Deployment Script
# This script sets up the environment and starts the Flask application

set -e  # Exit on any error

echo "🚨 DisasterAI Deployment Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check if pip is installed
print_status "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

print_success "pip3 found"

# Create virtual environment if it doesn't exist
print_status "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install required packages
print_status "Installing required packages..."
pip install -r requirements.txt
print_success "All packages installed successfully"

# Check if .env file exists
print_status "Checking environment configuration..."
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating template..."
    cat > .env << EOF
# DisasterAI Environment Variables
# Copy this file and update with your actual values

# Swisscom API Key for Apertus model
SWISSCOM_API=your_api_key_here

# Firebase Configuration (optional - will use in-memory storage if not set)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
EOF
    print_warning "Please edit .env file with your actual API keys and Firebase credentials"
    print_warning "For now, the app will use in-memory storage for chat history"
else
    print_success ".env file found"
fi

# Check if Firebase credentials file exists
print_status "Checking Firebase credentials..."
if [ ! -f "swiss-ai-hack-firebase-adminsdk-fbsvc-7a0fbd49d6.json" ]; then
    print_warning "Firebase credentials file not found"
    print_warning "The app will use in-memory storage for chat history"
else
    print_success "Firebase credentials file found"
fi

# Check if static directory exists and create if needed
print_status "Checking static files directory..."
if [ ! -d "static" ]; then
    print_status "Creating static directory..."
    mkdir -p static
    print_success "Static directory created"
fi

# Copy game.js to static directory if it exists
if [ -f "game.js" ] && [ ! -f "static/game.js" ]; then
    print_status "Copying game.js to static directory..."
    cp game.js static/
    print_success "game.js copied to static directory"
fi

# Copy sounds directory to static if it exists
if [ -d "sounds" ] && [ ! -d "static/sounds" ]; then
    print_status "Copying sounds directory to static..."
    cp -r sounds static/
    print_success "Sounds directory copied to static"
fi

# Check if templates directory exists
print_status "Checking templates directory..."
if [ ! -d "templates" ]; then
    print_error "Templates directory not found. Please ensure you're in the correct directory."
    exit 1
fi

print_success "Templates directory found"

# Check if app.py exists
print_status "Checking main application file..."
if [ ! -f "app.py" ]; then
    print_error "app.py not found. Please ensure you're in the correct directory."
    exit 1
fi

print_success "app.py found"

# Set default port
PORT=${PORT:-5001}

# Check if port is available
print_status "Checking if port $PORT is available..."
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warning "Port $PORT is already in use"
    print_status "Trying to find an available port..."
    
    # Try ports 5001-5010
    for port in {5001..5010}; do
        if ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            PORT=$port
            print_success "Found available port: $PORT"
            break
        fi
    done
    
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_error "No available ports found in range 5001-5010"
        print_error "Please stop the process using port $PORT or specify a different port"
        print_error "Usage: PORT=8080 ./deploy.sh"
        exit 1
    fi
else
    print_success "Port $PORT is available"
fi

# Export environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    print_status "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
    print_success "Environment variables loaded"
fi

# Create run_app.py if it doesn't exist
print_status "Creating run_app.py..."
cat > run_app.py << EOF
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
    port = int(os.environ.get('PORT', $PORT))
    
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
        print("\\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
EOF

print_success "run_app.py created"

# Make run_app.py executable
chmod +x run_app.py

# Start the application
print_status "Starting DisasterAI application..."
print_success "Deployment completed successfully!"
echo ""
echo "🎉 DisasterAI is now running!"
echo "=================================="
echo "🌐 Home Page: http://localhost:$PORT"
echo "🤖 Chatbot: http://localhost:$PORT/chatbot"
echo "🎮 Mario Game: http://localhost:$PORT/game"
echo ""
echo "🛑 To stop the server, press Ctrl+C"
echo ""

# Start the Flask application
python run_app.py
