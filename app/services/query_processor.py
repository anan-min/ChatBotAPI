from app.providers import OpenAIProvider
class QueryProcessor:
    def __init__(self, text) -> None:
        self.openai_provider = OpenAIProvider()
        self.text = text

    async def query_response(self):
        if False:
            pass
        else:
            return await self.openapi_query(self.text)
    
    async def openapi_query(self):
        return await self.openai_provider.query_text_file(self.text)