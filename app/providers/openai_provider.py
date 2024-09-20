from app.utilities import Timer 
from openai import OpenAI
import json



API_KEYS = ""
class OpenAIProvider:

    def __init__(self) -> None:
        self.client = OpenAI(api_key=API_KEYS)


    def transcribe_audio_file(self, audio_file):
        # timer start
        
        transcribed_data = self.client.audio.transcriptions.create(model='whisper-1', file=audio_file, response_format='verbose_json')

        return transcribed_data.text

        # timer end fw e
        # log rtt for transcribe 
        # where to store these file cloud in which format

    def query_text_file(self, text):
        completion = self.client.chat.completions.create(
        model="gpt-4",
            messages=[
                {"role": "system", "content": text},
                {"role": "user", "content": "Hello!"}
            ]
        )
        return completion
    

    def speech_synthesis(self, text):
        response = self.client.audio.speech.create(model='tts-1', voice="alloy", input=text)

        result = b''.join([chunk for chunk in response.iter_bytes()])

        return result
        



