import pytest
from pathlib import Path
from app.providers.google_provider import GoogleProvider

@pytest.fixture
def provider():
    return GoogleProvider()

def test_transcribe_audio_file_real_api(provider):
    audio_file_path = Path(__file__).parent.parent.parent / 'app' / 'data' / 'test' / 'voice.wav'
    transcribed_data = provider.transcribe_audio_file(audio_file_path)
    assert type(transcribed_data) == str
    assert len(transcribed_data) > 0

def test_speech_synthesis_real_api(provider):
    text = "This is a test of speech synthesis."
    synthesized_audio = provider.speech_synthesis(text)
    
    assert type(synthesized_audio) == bytes
    assert len(synthesized_audio) > 0
