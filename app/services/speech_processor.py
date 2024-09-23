from app.providers import OpenAIProvider

class SpeechProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()

    async def process(self, request_data, text):
        tts_provider = request_data.get_tts_provider()
        if False:
            pass 
        else:
            return await self.openai_tts(text)
    
    async def openai_tts(self, text):
        return await self.openai_provider.speech_synthesis(text) 