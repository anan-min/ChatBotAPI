from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()
API_KEYS = os.getenv('openai_api_key')
class OpenAIProvider:

    def __init__(self) -> None:
        print(f"openai api key: {API_KEYS}")


    def transcribe_audio_file(self, audio_file):
        # timer start
        
        transcribed_data = self.client.audio.transcriptions.create(model='whisper-1', file=audio_file, response_format='verbose_json')

        return transcribed_data.text

        

    def query_text_file(self, text):
        completion = self.client.chat.completions.create(
        model="gpt-4",
            messages=[
                {"role": "system", "content": text},
                {"role": "user", "content": "Hello!"}
            ]
        )
        return completion.choices[0].message.content
    

    def speech_synthesis(self, text):
        response = self.client.audio.speech.create(model='tts-1', voice="alloy", input=text)

        result = b''.join([chunk for chunk in response.iter_bytes()])

        return result
        



