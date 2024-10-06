import pytest
import asyncio
from pathlib import Path
from app.providers.openai_provider import OpenAIProvider

@pytest.fixture
def provider():
    return OpenAIProvider()

@pytest.mark.asyncio
async def test_transcribe_audio_file_real_api(provider):
    audio_file_path = Path(__file__).parent.parent.parent / 'app' / 'data' / 'test' / 'voice.wav'
    transcribed_data = await provider.transcribe_audio_file(audio_file_path)
    assert type(transcribed_data) == str
    assert len(transcribed_data) > 0

@pytest.mark.asyncio
async def test_query_text_file_real_api(provider):
    text = "Hello, how are you?"
    response = await provider.query_text_file(text)
    assert type(response) == str
    assert len(response) > 0

@pytest.mark.asyncio
async def test_speech_synthesis_real_api(provider):
    text = "This is a test of speech synthesis."
    synthesized_audio = await provider.speech_synthesis(text)

    assert type(synthesized_audio) == bytes
    assert len(synthesized_audio) > 0
