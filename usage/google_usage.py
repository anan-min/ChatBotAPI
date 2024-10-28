from app.providers.google_provider import GoogleProvider
import asyncio 
from pathlib import Path

sample_voices_path = Path(__file__).parent.parent / 'app' / 'data' / 'sample' 

async def test_async_google_stt():
    google_provider = GoogleProvider()
    transcribe_text = await google_provider.transcribe_audio_file(sample_voices_path)
    print(transcribe_text)

     

if __name__ == "__main__":
    asyncio.run(test_async_google_stt())