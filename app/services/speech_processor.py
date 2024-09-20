from app.providers import OpenAIProvider

class SpeechProcessor:
    def __init__(self, text, tts_provider) -> None:
        self.openai_provider = OpenAIProvider()
        self.tts_provider = tts_provider

    async def convert_to_speech(self):
        if False:
            pass 
        else:
            return await self.openai_tts(self.text)
    
    async def openai_tts(self, text):
        return await self.openai_provider.speech_synthesis(text) 