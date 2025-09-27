# Disaster Management Chatbot

A Flask-based chatbot application for disaster management assistance, powered by Swisscom's Apertus AI and Firebase for data storage.

## Features

- 🤖 AI-powered disaster management assistance
- 💬 Real-time chat interface with context awareness
- 🔥 Firebase integration for chat history storage
- 📱 Responsive design for mobile and desktop
- 🚨 Real-time disaster information and response strategies

## Setup

### Prerequisites

- Python 3.8+
- Swisscom API key (optional - app will work without it but API calls will fail)
- Firebase project with Realtime Database (optional - app has in-memory fallback)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
export SWISSCOM_API="your_swisscom_api_key_here"
```

3. Ensure Firebase credentials file is in the same directory as `app.py` (optional):
   - File: `swiss-ai-hack-firebase-adminsdk-fbsvc-7a0fbd49d6.json`
   - If not present, app will use in-memory storage

4. Run the application:
```bash
python run_app.py
```

5. Open your browser and navigate to:
   - Home page: `http://localhost:5000`
   - Chatbot: `http://localhost:5000/chatbot`

### Quick Test

Test the application:
```bash
python test_chat.py
```

### Setup API Key

To enable AI responses, set up your Swisscom API key:
```bash
python setup_api_key.py
```

Or manually set the environment variable:
```bash
export SWISSCOM_API="your_api_key_here"
```

## API Endpoints

- `GET /` - Home page with navigation
- `GET /chatbot` - Chatbot interface
- `POST /chat` - Chat API endpoint

### Chat API Request Format:
```json
{
    "message": "Your question here",
    "chat_id": "optional_chat_id"
}
```

### Chat API Response Format:
```json
{
    "response": "AI response text",
    "error": false
}
```

## Firebase Schema

The application stores chat data in Firebase Realtime Database with the following structure:

```
chats/
  {chat_id}/
    {timestamp}/
      input: "user message"
      output: "ai response"
      timestamp: 1234567890
```

## Configuration

- Update `DISASTER_CONTEXT` in `app.py` to modify the disaster information available to the AI
- Modify Firebase database URL in the Firebase initialization if needed
- Adjust AI model parameters in the chat API endpoint

## Troubleshooting

1. **Firebase Connection Issues**: Ensure the database URL is correct and the service account has proper permissions
2. **API Key Issues**: Verify the Swisscom API key is set correctly in environment variables
3. **Import Errors**: Install all required dependencies using `pip install -r requirements.txt`
