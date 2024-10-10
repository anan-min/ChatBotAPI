import os
from google.cloud import texttospeech, speech_v1 as speech

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
api_credentials = os.path.join(base_dir, 'api', 'google', 'demo.json')

voice_configs = {
    "language_code":"th-TH",
    "ssml_gender": getattr(texttospeech.SsmlVoiceGender, "NEUTRAL")
}

audio_configs = {
    "audio_encoding": texttospeech.AudioEncoding.MP3,
    "speaking_rate": 1.0,
    "pitch":1.0,
    "effects_profile_id": "standard"
}

transcribe_configs = {
    "encoding":speech.RecognitionConfig.AudioEncoding.LINEAR16,
    "sample_rate_hertz":16000,
    "language_code":"th-TH",
    "model": "default" 
}