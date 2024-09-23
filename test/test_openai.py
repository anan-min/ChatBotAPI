from pathlib import Path
from app.providers import OpenAIProvider
import io
import base64


def test_openai_provider():
    provider = OpenAIProvider()

    audio_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'voice.wav'
    audio_file = open(audio_file_path, "rb")

    text = provider.transcribe_audio_file(audio_file)
    print(f"transcribe text: {text}")

    response = provider.query_text_file(text)

    print(response)
    print(f"openai response: {response}")


    speech_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'speech.wav'
    speech = provider.speech_synthesis(response)
    with open(speech_file_path, 'wb') as speech_file:
                speech_file.write(speech)
                
    print(f"speech generated at{speech_file_path}")


def test_audio_bytes():
    provider = OpenAIProvider()
    audio_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'voice.wav'
    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()
    encoded_audio = base64.b64encode(audio_data)
    decoded_audio_bytes = base64.b64decode(encoded_audio)

    transcription = provider.transcribe_audio_file(decoded_audio_bytes)
    print(transcription)
    assert transcription is not None, "Transcription should not be None"

# test_openai_provider()
test_audio_bytes()
