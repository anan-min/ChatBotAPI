from pathlib import Path
from app.providers import OpenAIProvider
from app.providers.google_provider import GoogleProvider
import io
import asyncio
import base64


async def test_openai_provider():
    provider = GoogleProvider()
    openai = OpenAIProvider()

    # audio_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'voice2.wav'

    # text = provider.transcribe_audio_file(audio_file_path)
    # print(f"transcribe text: {text}")

    # response = await openai.query_text_file(text)

    # print(response)
    # print(f"openai response: {response}")


    speech_file_path = Path(__file__).parent.parent / 'app' / 'data' / 'test' / 'speech.wav'
    speech = provider.speech_synthesis("ลองพูดสิ่งนี้ดูสิว่าจะมีเสียงอย่างไร")
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


asyncio.run(test_openai_provider())
