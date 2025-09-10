from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
import time

load_dotenv()
API_KEYS = os.getenv('openai_api_key')


class OpenAIProvider:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=API_KEYS)

    async def transcribe_audio_file(self, audio_file_path):
        start_time = time.time()
        loop = asyncio.get_running_loop()
        transcribed_data = await loop.run_in_executor(
            None,
            self._transcribe_sync,
            audio_file_path
        )
        end_time = time.time()

        return transcribed_data

    def _transcribe_sync(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:

            return self.client.audio.transcriptions.create(
                model='whisper-1',
                file=audio_file,
                response_format='verbose_json'
            ).text

    async def query_text_file(self, text):
        # Since OpenAI's client library is not inherently asynchronous, run in executor
        system_prompt = (
            "You are a male virtual assistant for SCG Group in Thailand. "
            "You respond to user questions and requests clearly and politely in Thai or English, as appropriate. "
            "Your answers are delivered as text, which will be converted to speech for the user. "
            "Sometimes, users may say things that are not related to SCG or may be testing the system; "
            "always reply helpfully and professionally, even if the input seems irrelevant. "
            "\n\nSCG Company Information:\n"
            "เอสซีจี หรือ บริษัท ปูนซิเมนต์ไทย จำกัด (มหาชน) (อังกฤษ: Siam Cement Group ชื่อย่อ: SCG) เป็นบริษัทปูนซีเมนต์และวัสดุก่อสร้างที่ใหญ่ที่สุดและเก่าแก่ที่สุดในประเทศไทยและเอเชียตะวันออกเฉียงใต้ ในปี 2559 เอสซีจียังได้รับการจัดอันดับให้เป็นบริษัทที่ใหญ่เป็นอันดับ 2 ของประเทศไทย และเป็นบริษัทมหาชนอันดับที่ 604 ของโลกโดย ฟอบส์ บริษัทอยู่ในดัชนี SET50 และ SETHD ในหมวดอุตสาหกรรม ผู้ถือหุ้นใหญ่ของบริษัท (ร้อยละ 30) คือพระบาทสมเด็จพระวชิรเกล้าเจ้าอยู่หัว"
        )
        loop = asyncio.get_running_loop()
        completion = await loop.run_in_executor(
            None,
            lambda: self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ]
            )
        )
        return completion.choices[0].message.content

    async def speech_synthesis(self, text):
        # Same as above, handle potentially synchronous calls in an executor
        loop = asyncio.get_running_loop()
        start_time = time.time()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.audio.speech.create(
                model='tts-1', voice="onyx", input=text)
        )
        end_time = time.time()
        result = b''.join([chunk for chunk in response.iter_bytes()])
        return result
