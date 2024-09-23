from openai import OpenAI
from dotenv import load_dotenv
import os 
import asyncio
import time 

load_dotenv()
API_KEYS = os.getenv('openai_api_key')

class OpenAIProvider:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=API_KEYS)
 
    async def transcribe_audio_file(self, audio_file_path):
        start_time = time.time()
        loop = asyncio.get_running_loop()
        transcribed_data = await loop.run_in_executor(
            None,  
            self._transcribe_sync,  
            audio_file_path 
        )
        end_time = time.time()
        print(f"Transcription from openapi took {end_time - start_time} seconds to complete")

        return transcribed_data
    
    def _transcribe_sync(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            
            return self.client.audio.transcriptions.create(
                model='whisper-1',
                file=audio_file,
                response_format='verbose_json'
            ).text
    
    async def query_text_file(self, text):
        # Since OpenAI's client library is not inherently asynchronous, run in executor
        loop = asyncio.get_running_loop()
        completion = await loop.run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": text},
                ]
            )
        )
        return completion.choices[0].message.content

    async def speech_synthesis(self, text):
        # Same as above, handle potentially synchronous calls in an executor
        loop = asyncio.get_running_loop()
        start_time = time.time()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.audio.speech.create(model='tts-1', voice="alloy", input=text)
        )
        end_time = time.time()
        print(f"Speech synthesis from openai took {end_time - start_time} seconds to complete")
        result = b''.join([chunk for chunk in response.iter_bytes()])
        return result


