from app.providers import OpenAIProvider

class TranscribeProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider() 

    
    async def transcribe(self, request_data):
        audio_file = request_data.get_audio_file()
        if False:
            pass 
        else:
            return await self.openai_transcribe(self.audio_file)


    async def openai_transcribe(self, audio_file):
        return self.openai_provider.transcribe_audio_file(audio_file)
    
