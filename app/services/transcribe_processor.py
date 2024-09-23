from app.providers import OpenAIProvider
from app.utils import files_handler
from pathlib import Path

class TranscribeProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider() 

    
    async def process(self, request_data):
        audio_file = request_data.get_audio_file()
        provider_name = request_data.get_stt_provider()

        if provider_name == 'google':
            return await self.google_transcribe(audio_file)
        elif provider_name == 'azure':
            return await self.azure_transcribe(audio_file)
        elif provider_name == 'aws':
            return await self.aws_transcribe(audio_file)
        else:
            return await self.openai_transcribe(audio_file)
  

    async def openai_transcribe(self, audio_file):
        audio_file_path = files_handler.save_audio_file(audio_file)
        try:
            return await self.openai_provider.transcribe_audio_file(audio_file_path)
        finally:
            files_handler.delete_file(audio_file_path)
    
    async def google_transcribe(self, audio_file_path):
        pass

    async def azure_transcribe(self, audio_file_path):
        pass

    async def aws_transcribe(self, audio_file_path):
        pass
    
