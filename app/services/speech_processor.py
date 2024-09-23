from app.providers import OpenAIProvider

class SpeechProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()

    async def convert_to_speech(self, tts_provider, text):
        if False:
            pass 
        else:
            return await self.openai_tts(text)
    
    async def openai_tts(self, text):
        return await self.openai_provider.speech_synthesis(text) 