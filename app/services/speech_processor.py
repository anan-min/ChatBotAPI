from app.providers import OpenAIProvider
from app.utils.session_manager import SessionManager

class SpeechProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()

    async def process(self, session: SessionManager):
        tts_provider = session.get_tts_provider()
        text = session.get_query_text()
        if False:
            pass 
        else:
            speech =  await self.openai_tts(text)
            session.set_query_speech(speech)
    
    async def openai_tts(self, text):
        return await self.openai_provider.speech_synthesis(text) 