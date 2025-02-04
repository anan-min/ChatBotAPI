import aiohttp
import asyncio

ollama_url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

class OllamaProvider:
    def __init__(self):
        pass

    async def query_text_file(self, text, model="llama3.2"):
        data = {
            "model": model,
            "prompt": text,
            "stream": False
        }

        # Using aiohttp to make an asynchronous request
        async with aiohttp.ClientSession() as session:
            async with session.post(ollama_url, headers=headers, json=data) as response:
                if response.status == 200:
                    response_json = await response.json()
                    generated_text = response_json.get("response", "No content in response")
                    return generated_text
                else:
                    return f"Error: {response.status}, {await response.text()}"

