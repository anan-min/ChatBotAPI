import aioboto3
import asyncio
import os
import aiohttp
import time
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

class AmazonProvider:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.region_name = 'ap-southeast-2'

    async def transcribe_audio_file(self, audio_file_path):
        job_name = "transcribe-job-" + str(int(time.time() * 1000))
        job_uri = await self.store_audio_as_uri(audio_file_path)
        print(f"Started transcription job: {job_name} for URI: {job_uri}")

        async with aioboto3.client('transcribe', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                    region_name=self.region_name) as stt:
            await stt.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat='wav',
                LanguageCode='th-TH'
            )

            return await self.process_response(stt, job_name, 5)

    async def process_response(self, stt, job_name, check_interval):
        print(f"Checking transcription status for job: {job_name}")
        while True:
            status = await stt.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                print(f"Transcription job {job_name} status: {status['TranscriptionJob']['TranscriptionJobStatus']}")
                break
            await asyncio.sleep(check_interval)

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print(f"Transcription completed. Transcript available at: {transcript_file_uri}")
            return await self.parse_transcript_uri(transcript_file_uri)
        else:
            print(f"Transcription job failed: {status['TranscriptionJob']['FailureReason']}")
            return None

    async def parse_transcript_uri(self, transcript_file_uri):
        print(f"Parsing transcript URI: {transcript_file_uri}")
        async with aiohttp.ClientSession() as session:
            async with session.get(transcript_file_uri) as response:
                if response.status != 200:
                    print(f"Error fetching transcript: HTTP {response.status}")
                    return None
                transcript_data = await response.json()
                transcript_text = transcript_data['results']['transcripts'][0]['transcript']
                print(f"Transcript text: {transcript_text}")
                return transcript_text

    async def store_audio_as_uri(self, audio_file_path):
        file_name = os.path.basename(audio_file_path)
        s3_key = f"audio/{file_name}"

        async with aioboto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                    region_name=self.region_name) as s3_client:
            try:
                await s3_client.upload_file(str(audio_file_path), self.bucket_name, s3_key)
                print(f"Audio file {file_name} uploaded to S3 at: s3://{self.bucket_name}/{s3_key}")
            except Exception as e:
                print(f"Error uploading file to S3: {e}")
                return None

        return f"s3://{self.bucket_name}/{s3_key}"

if __name__ == "__main__":
    bucket_name = "speech-to-text-storage"
    s3_helper = AmazonProvider(bucket_name)
