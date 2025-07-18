from providers.openai_provider import OpenAIProvider
from providers.amazon_provider import AmazonProvider
from providers.google_provider import GoogleProvider
import utils.files_handler as files_handler
from pathlib import Path
from utils.session_manager import SessionManager


class TranscribeProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()
        bucket_name = 'speech-to-text-storage'
        self.amazon_provider = AmazonProvider(bucket_name)
        self.google_provider = GoogleProvider()

    async def process(self, session: SessionManager):
        audio_file = session.get_client_audio_file()
        provider_name = session.get_stt_provider()

        print(f"transcribe_provider_name: {provider_name}")

        result = None
        if provider_name == "openai_stt":
            print("using openai_stt")
            result = await self.openai_transcribe(audio_file)
        elif provider_name == 'google_stt':
            print("using google_stt")
            result = await self.google_transcribe(audio_file)
        elif provider_name == 'aws_stt':
            result = await self.aws_transcribe(audio_file)
        else:
            print("using google_stt")
            result = await self.google_transcribe(audio_file)
        session.set_transcribe_text(result)

    async def openai_transcribe(self, audio_file):
        audio_file_path = files_handler.save_audio_file(audio_file)
        try:
            return await self.openai_provider.transcribe_audio_file(audio_file_path)
        finally:
            files_handler.delete_file(audio_file_path)

    async def google_transcribe(self, audio_file):
        return await self.google_provider.transcribe_audio_file(audio_file)

    async def azure_transcribe(self, audio_file):
        pass

    async def aws_transcribe(self, audio_file):
        audio_file_path = files_handler.save_audio_file(audio_file)
        try:
            return await self.amazon_provider.transcribe_audio_file(audio_file_path)
        finally:
            files_handler.delete_file(audio_file_path)
