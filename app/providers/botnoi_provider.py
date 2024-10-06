import requests
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
        # ใช้ asyncio.run_in_executor เพื่อทำให้ synchronous API เรียกใช้ในรูปแบบ async
        loop = asyncio.get_running_loop()

        start_time = time.time()
        response = await loop.run_in_executor(
            None,
            lambda: self._sync_speech_synthesis(text)  # เรียกฟังก์ชัน synchronous
        )
        end_time = time.time()
        print(f"Speech synthesis from Botnoi took {end_time - start_time} seconds to complete")
        return response

    def _sync_speech_synthesis(self, text):
        # ฟังก์ชัน synchronous ที่เรียกใช้ API ด้วย requests
        payload = {
            "text": text,
            "speaker": "1",  # เลือก speaker reccommend 1 หรือ 4
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

        # ใช้ requests.post แบบ synchronous
        response = requests.post(self.url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            audio_url = result.get('audio_url')
            
            # ดึงไฟล์เสียงจาก URL
            if audio_url:
                audio_response = requests.get(audio_url)
                if audio_response.status_code == 200:
                    return audio_response.content  # คืนค่าไฟล์เสียงเป็น bytes
            return None
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

