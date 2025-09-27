# 🚨 Disaster Management Chatbot Setup Guide

## Quick Fix for "AI service not available" Error

The error "Sorry, the AI service is not available" occurs because the `SWISSCOM_API` environment variable is not set. Here's how to fix it:

## 🔧 **Method 1: Set Environment Variable (Quick Fix)**

```bash
# Set the API key for current session
export SWISSCOM_API="your_actual_swisscom_api_key_here"

# Run the app
python run_app.py
```

## 🔧 **Method 2: Create .env File (Permanent Fix)**

1. Create a file named `.env` in the `dev/src/input_LLM/` directory
2. Add this content to the file:
   ```
   SWISSCOM_API=your_actual_swisscom_api_key_here
   ```
3. Replace `your_actual_swisscom_api_key_here` with your real API key
4. Run the app:
   ```bash
   python run_app.py
   ```

## 🔧 **Method 3: Use Setup Script**

```bash
python setup_env.py
```

## 🧪 **Test the Setup**

After setting up the API key, test the application:

```bash
python test_chat.py
```

## 📋 **What You Need**

1. **Swisscom API Key**: Get this from your Swisscom account
2. **Valid API Key**: The key should work with the Apertus model endpoint

## 🔍 **Troubleshooting**

### If you get "API key is invalid":
- Check that your API key is correct
- Ensure the key has access to the Apertus model
- Verify the key is not expired

### If you get "Apertus model endpoint not available":
- Check the API endpoint URL
- Verify your account has access to the Apertus model
- Contact Swisscom support if needed

### If you get "AI service is not available":
- The `SWISSCOM_API` environment variable is not set
- Follow Method 1 or 2 above to set it

## 🚀 **Quick Start (No API Key)**

If you want to test the app without an API key, it will show a helpful message instead of AI responses. The UI and Firebase functionality will still work.

## 📞 **Need Help?**

1. Check the console output for detailed error messages
2. Verify your API key is correct
3. Ensure you have access to the Swisscom Apertus model
4. Check the Swisscom API documentation for any changes

---

**Note**: The app will work without an API key, but you'll get placeholder responses instead of real AI-generated content.
