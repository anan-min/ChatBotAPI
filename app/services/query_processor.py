from app.providers import OpenAIProvider
from app.utils.session_manager import SessionManager
class QueryProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()

    async def process(self, session: SessionManager):
        query_provider = session.get_query_provider()
        text = session.get_transcribe_text()
        if False:
            pass
        else:
           text = await self.openapi_query(text)
           session.set_query_text(text)
    
    async def openapi_query(self, text):
        return await self.openai_provider.query_text_file(text)