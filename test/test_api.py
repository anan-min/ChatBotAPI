from app.providers import OpenAIProvider
from pathlib import Path
import base64
import requests

url = 'http://127.0.0.1:5000/'
audio_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'voice.wav'

def test_openai_api_flow():
    with open(audio_file_path, 'rb') as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        # Create JSON payload
    payload = {
        "stt_provider": "openai",
        "tts_provider": "openai",
        "query_provider": "openai",
        "audio_file": encoded_audio
    }
    response = requests.post(url, json=payload)

# Call the function to test the API
test_openai_api_flow()
