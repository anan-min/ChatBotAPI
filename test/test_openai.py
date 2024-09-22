from test_path import add_path
add_path()
from pathlib import Path
from app.providers import OpenAIProvider



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





test_openai_provider()
