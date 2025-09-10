# ChatBot API

A Python-based chatbot API that integrates multiple AI providers including OpenAI, Google Cloud, Amazon AWS, Botnoi, and Ollama for speech-to-text, text-to-speech, and language model capabilities.

## Setup Instructions

### 1. Environment Variables Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your API keys:
   ```bash
   # OpenAI API Key
   openai_api_key=your_openai_api_key_here

   # Botnoi API Key
   BOTNOI_API_KEY=your_botnoi_api_key_here

   # AWS Credentials
   AWS_ACCESS_KEY_ID=your_aws_access_key_here
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here

   # Ollama Model (optional, defaults to qwen2.5:3b)
   OLLAMA_MODEL=qwen2.5:3b
   ```

### 2. Google API Credentials Setup

1. Copy the example Google API key file:
   ```bash
   cp google_api_key.json.example google_api_key.json
   ```

2. Replace the content of `google_api_key.json` with your actual Google Cloud service account credentials.

   **Note:** Get your credentials from [Google Cloud Console](https://console.cloud.google.com/) by creating a service account with the following APIs enabled:
   - Text-to-Speech API
   - Speech-to-Text API  
   - Natural Language API

### 3. Install FFmpeg (Required for Audio Processing)

FFmpeg is required for audio file processing. Choose one of the following methods:

#### Method 1: Using Winget (Recommended - Built into Windows 10/11)
```bash
winget install ffmpeg
```

#### Method 2: Using Chocolatey (Alternative)
1. **Install Chocolatey** (if not already installed):
   Open PowerShell as Administrator and run:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install FFmpeg:**
   ```bash
   choco install ffmpeg
   ```

#### Method 3: Manual Installation (Last Resort)
1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your Windows PATH environment variable
4. Restart your terminal

**Verify Installation:**
```bash
ffmpeg -version
```

### 4. Virtual Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 5. Run the Application

Navigate to the app directory and run the main application:
```bash
cd app
python main.py
```

The API will be available at `http://localhost:5000`

## Project Structure

```
ChatBotAPI/
├── app/
│   ├── main.py              # Main application entry point
│   ├── routes.py            # API routes
│   ├── providers/           # AI service providers
│   ├── services/            # Business logic services
│   └── utils/               # Utility functions
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Example environment variables
├── google_api_key.json      # Google Cloud credentials (create from example)
├── google_api_key.json.example # Example Google Cloud credentials
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## API Providers

- **OpenAI**: Text-to-speech and language models
- **Google Cloud**: Speech-to-text, text-to-speech, and natural language processing
- **Amazon AWS**: Speech transcription services
- **Botnoi**: Thai text-to-speech services
- **Ollama**: Local language models (Qwen2.5, Llama3.2)

## Development

The application uses Quart framework for async API handling and supports CORS for frontend integration at `http://localhost:3000`.

For testing individual providers, check the `usage/` directory for example scripts.
