from app.providers import OpenAIProvider
class QueryProcessor:
    def __init__(self) -> None:
        self.openai_provider = OpenAIProvider()

    async def process(self, request_data ,text):
        query_provider = request_data.get_query_provider()
        if False:
            pass
        else:
            return await self.openapi_query(text)
    
    async def openapi_query(self, text):
        return await self.openai_provider.query_text_file(text)