from app.providers import OpenAIProvider
from app.providers.ollama_provider import OllamaProvider
from app.utils.session_manager import SessionManager
class QueryProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()
        self.ollama_provider = OllamaProvider()

    async def process(self, session: SessionManager):
        query_provider = session.get_query_provider()
        text = session.get_transcribe_text()
        if query_provider == 'llama':
            print("Query provider is ollama")
            text = await self.ollama_query(text)
            session.set_query_text(text)
        else:
            print("Query provider is openai")
            text = await self.openapi_query(text)
            session.set_query_text(text)
    
    async def openapi_query(self, text):
        return await self.openai_provider.query_text_file(text)

    async def ollama_query(self, text):
        return await self.ollama_provider.query_text_file(text)