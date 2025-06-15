from providers.openai_provider import OpenAIProvider
from providers.ollama_provider import OllamaProvider
from utils.session_manager import SessionManager
class QueryProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()
        self.ollama_provider = OllamaProvider()

    async def process(self, session: SessionManager):
        query_provider = session.get_query_provider()
        text = session.get_transcribe_text()

        print(f"using query provider: {query_provider}")

        if query_provider == 'openai':
            await self.openai_query(text, session)
        elif query_provider == "qwen25":
            await self.qwen25_query(text, session)
        elif query_provider == "llama":
            await self.llama_query(text, session)
        else:
            await self.openai_query(text, session)
    
    async def openai_query(self, text, session):
        text = await self.openai_provider.query_text_file(text)
        session.set_query_text(text)  

    async def qwen25_query(self, text, session):
        text =  await self.ollama_provider.query_qwen25(text)
        session.set_query_text(text) 

    async def llama_query(self, text, session):
        text =  await self.ollama_provider.query_llama32(text)
        session.set_query_text(text) 
     

    