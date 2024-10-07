from app.services import RequestProcessor
from pathlib import Path

def test_parse_data():
    audio_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'voice.wav'
    audio_file = open(audio_file_path, "rb")


    request_processor = RequestProcessor()
    request_data = {
        "stt_provider": "openai",
        "tts_provider": "openai",
        "query_provider": "openai",
        "audio-file": "test/test_audio.mp3"
    }

    request = request_processor.parse_data(request_data)
    print(request)
    
