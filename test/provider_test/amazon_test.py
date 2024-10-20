import pytest
import asyncio
from pathlib import Path
from jiwer import wer  # ใช้สำหรับคำนวณ Word Error Rate (WER)
from app.providers.amazon_provider import AmazonProvider
import csv
from fuzzywuzzy import fuzz

@pytest.fixture
def provider():
    bucket_name = "speech-to-text-storage"
    return AmazonProvider(bucket_name)


@pytest.mark.asyncio
async def test_transcribe_audio_file_real_api(provider):
    audio_file_path = Path(__file__).parent.parent.parent / 'app' / 'data' / 'test' / 'voice.wav'
    transcribed_data = await provider.transcribe_audio_file(audio_file_path)
    assert isinstance(transcribed_data, str)
    assert len(transcribed_data) > 0

def test_store_audio_as_uri(provider):
    audio_file_path = Path(__file__).parent.parent.parent / 'app' / 'data' / 'test' / 'voice.wav'
    uri = provider.store_audio_as_uri(audio_file_path)
    assert uri.startswith('s3://'), f"Expected S3 URI but got {uri}"
    assert 'audio/' in uri, f"Expected audio path in S3 URI but got {uri}"

@pytest.mark.asyncio
async def test_process_response_failed(provider, mocker):
    mocker.patch.object(provider.stt, 'get_transcription_job', return_value={
        'TranscriptionJob': {'TranscriptionJobStatus': 'FAILED', 'FailureReason': 'Error'}
    })
    result = await provider.process_response('test-job', 1)
    assert result is None, "Expected None when job failed"



