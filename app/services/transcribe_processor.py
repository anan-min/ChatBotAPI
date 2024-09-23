from app.providers import OpenAIProvider
from app.utilities import files_handler
from pathlib import Path

class TranscribeProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider() 

    
    async def process(self, request_data):
        audio_file = request_data.get_audio_file()
        audio_file_path = files_handler.save_audio_file(audio_file)
        try:
            response = await self.openai_transcribe(audio_file_path)
            return response
        finally:
            files_handler.delete_file(audio_file_path)

    async def openai_transcribe(self, audio_file_path):
        return await self.openai_provider.transcribe_audio_file(audio_file_path)
    
