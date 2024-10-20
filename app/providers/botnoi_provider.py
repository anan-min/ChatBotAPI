import aiohttp
import asyncio
import os
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("BOTNOI_API_KEY")
url = "https://api-voice.botnoi.ai/openapi/v1/generate_audio"


class BotnoiProvider:
    def __init__(self):
        self.api_key = api_key
        self.url = url

    async def speech_synthesis(self, text):
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            response = await self._async_speech_synthesis(session, text)
        end_time = time.time()
        print(f"Speech synthesis from Botnoi took {end_time - start_time} seconds to complete")
        return response

    async def _async_speech_synthesis(self, session, text):
        payload = {
            "text": text,
            "speaker": "1",  # Choose speaker
            "volume": 1,
            "speed": 1,
            "type_media": "wav",
            "save_file": "true",
            "language": "th"
        }
        headers = {
            'Botnoi-Token': self.api_key,
            'Content-Type': 'application/json'
        }

        # Use aiohttp.post for asynchronous requests
        async with session.post(self.url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                audio_url = result.get('audio_url')

                # Fetch audio file from URL
                if audio_url:
                    audio_response = await session.get(audio_url)
                    if audio_response.status == 200:
                        return await audio_response.read()  # Return audio file as bytes
            else:
                print(f"Error {response.status}: {await response.text()}")
                return None


# Example usage of BotnoiProvider
async def main():
    botnoi = BotnoiProvider()
    audio_data = await botnoi.speech_synthesis("Hello, this is synthesized speech from Botnoi.")
    if audio_data:
        with open("output.wav", "wb") as f:
            f.write(audio_data)


if __name__ == "__main__":
    asyncio.run(main())
