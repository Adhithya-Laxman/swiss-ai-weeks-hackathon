# DisasterAI Deployment Guide

## Quick Start

### 1. Run the Deployment Script
```bash
./deploy.sh
```

### 2. Access the Application
- **Home Page**: http://localhost:5001
- **Chatbot**: http://localhost:5001/chatbot
- **Mario Game**: http://localhost:5001/game

## Manual Setup (Alternative)

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file with your API keys:
```bash
SWISSCOM_API=your_api_key_here
```

### 4. Start the Application
```bash
python run_app.py
```

## Environment Variables

### Required
- `SWISSCOM_API`: Your Swisscom API key for the Apertus model

### Optional
- `PORT`: Port number (default: 5001)
- `FIREBASE_PROJECT_ID`: Firebase project ID
- `FIREBASE_PRIVATE_KEY_ID`: Firebase private key ID
- `FIREBASE_PRIVATE_KEY`: Firebase private key
- `FIREBASE_CLIENT_EMAIL`: Firebase client email
- `FIREBASE_CLIENT_ID`: Firebase client ID

## Features

### 🏠 Home Page
- Landing page with navigation to chatbot and game
- Modern, responsive design

### 🤖 Chatbot
- AI-powered disaster management assistant
- Firebase integration for chat history
- Markdown-formatted responses
- Context-aware responses based on disaster data

### 🎮 Mario Game
- Interactive disaster exploration game
- Smart state management
- Integration with chatbot
- Sound effects and animations

## Troubleshooting

### Port Already in Use
```bash
PORT=8080 ./deploy.sh
```

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Firebase Issues
The app will automatically fall back to in-memory storage if Firebase is not configured.

### API Key Issues
Make sure your `SWISSCOM_API` is set in the `.env` file.

## File Structure
```
input_LLM/
├── app.py                 # Main Flask application
├── run_app.py            # Application runner
├── deploy.sh             # Deployment script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── templates/            # HTML templates
│   ├── index.html
│   ├── chatbot.html
│   ├── game.html
│   └── game_chatbot.html
├── static/               # Static files
│   ├── game.js
│   └── sounds/
└── output.json          # Disaster context data
```

## Support

For issues or questions, check the application logs or contact the development team.
