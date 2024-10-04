import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("BOTNOI_API_KEY")  
url = "https://api-voice.botnoi.ai/openapi/v1/generate_audio"





class BotnoiProvider:

    def speech_synthesis(self, text):
        if not api_key:
            raise ValueError("API Key not found. Please check your .env file.")

        payload = {
            "text": text,
            "speaker": "1",  #  1 หรือ 4 
            "volume": 1,
            "speed": 1,
            "type_media": "wav",
            "save_file": "true",
            "language": "th"
        }
        headers = {
            'Botnoi-Token': api_key,
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            print(result)
            return result.get('audio_url')
        else:
            print(f"Error {response.status_code}: {response.content}")
            return None



    def download_audio_file(self, audio_url, output_filename):
        audio_response = requests.get(audio_url)

        if audio_response.status_code == 200:
            output_folder = 'app/data/tts_audio' 
            
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, 'wb') as file:
                file.write(audio_response.content)
            print(f"ไฟล์เสียงถูกบันทึกไว้ที่: {output_path}")
        else:
            print(f"ไม่สามารถดาวน์โหลดไฟล์เสียงได้: {audio_response.status_code}")



    