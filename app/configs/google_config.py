import os
from pathlib import Path
from google.cloud import texttospeech, speech_v1 as speech

current_dir = Path(__file__).resolve().parent
api_credentials = str(current_dir / 'google_api_key.json')

voice_configs = {
    "language_code": "th-TH",
    "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL
}

audio_configs = {
    "audio_encoding": texttospeech.AudioEncoding.MP3,
    "speaking_rate": 1.0,
    "pitch": 0.0,  # Use 0 to simplify testing
    "effects_profile_id": []
}

transcribe_configs = {
    "encoding":speech.RecognitionConfig.AudioEncoding.LINEAR16,
    "sample_rate_hertz":16000,
    "language_code":"th-TH",
    "model": "default" 
}