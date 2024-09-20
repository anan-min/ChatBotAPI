from app.providers import OpenAIProvider

class TranscribeProcessor:
    def __init__(self, request_data) -> None:
        self.openai_provider = OpenAIProvider() 
        self.request_data = request_data
        self.audio_file = request_data.get_audio_file()
        self.stt_provider = request_data.get_stt_provider()

    
    async def transcribe(self):
        if False:
            pass 
        else:
            return await self.openai_transcribe(self.audio_file)


    async def openai_transcribe(self, audio_file):
        return self.openai_provider.transcribe_audio_file(audio_file)
    
