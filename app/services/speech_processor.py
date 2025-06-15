from providers.openai_provider import OpenAIProvider
from providers.botnoi_provider import BotnoiProvider
from providers.google_provider import GoogleProvider
from utils.session_manager import SessionManager

class SpeechProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()
        self.botnoi_provider = BotnoiProvider()
        self.google_provider = GoogleProvider()

    async def process(self, session: SessionManager):
        tts_provider = session.get_tts_provider()
        text = session.get_query_text()
        
        print(f"tts_provider: {tts_provider}")

        if tts_provider == 'openai_tts':
            await self.openai_tts(text, session)
        elif tts_provider == "google_tts":
            await self.google_tts(text, session)
        else:
            await self.google_tts(text, session)
        

    async def openai_tts(self, text, session):
        session.set_query_speech(await self.openai_provider.speech_synthesis(text))

    async def botnoi_tts(self, text, session):
        session.set_query_speech(await self.botnoi_provider.speech_synthesis(text))

    async def google_tts(self, text, session):
        session.set_query_speech(await self.google_provider.speech_synthesis(text))

