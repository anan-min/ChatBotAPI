from app.providers import OpenAIProvider, BotnoiProvider
from app.providers.google_provider import GoogleProvider
from app.utils.session_manager import SessionManager

class SpeechProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()
        self.botnoi_provider = BotnoiProvider()
        self.google_provider = GoogleProvider()

    async def process(self, session: SessionManager):
        tts_provider = session.get_tts_provider()
        text = session.get_query_text()
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(text)
        print(tts_provider)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

        if tts_provider == 'botnoi':
            await self.botnoi_tts(text, session)
        elif tts_provider == 'google':
            await self.google_tts(text, session)
        else:
            await self.openai_tts(text, session)
        

    async def openai_tts(self, text, session):
        session.set_query_speech(await self.openai_provider.speech_synthesis(text))

    async def botnoi_tts(self, text, session):
        session.set_query_speech(await self.botnoi_provider.speech_synthesis(text))

    async def google_tts(self, text, session):
        session.set_query_speech(self.google_provider.speech_synthesis(text))

