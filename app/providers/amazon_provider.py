import boto3
import time
from urllib.parse import urlparse
import json
from dotenv import load_dotenv
import os
import requests
import asyncio

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class AmazonProvider:
    def __init__(self, bucket_name):
        self.stt = boto3.client(
            'transcribe',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='ap-southeast-2'
        )
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

    # Asynchronous transcription method
    async def transcribe_audio_file(self, audio_file_path):
        job_name = "transcribe-job-" + str(int(time.time() * 1000))
        job_uri = await self.store_audio_as_uri(audio_file_path)
        print(f"Started transcription job: {job_name} for URI: {job_uri}")

        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.stt.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat='wav',
                LanguageCode='th-TH'
            )
        )

        return await self.process_response(job_name, 5)

    # Asynchronous response processing
    async def process_response(self, job_name, check_interval):
        print(f"Checking transcription status for job: {job_name}")
        while True:
            status = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.stt.get_transcription_job(TranscriptionJobName=job_name)
            )
            job_status = status['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                print(f"Transcription job {job_name} status: {job_status}")
                break
            await asyncio.sleep(check_interval)

        if job_status == 'COMPLETED':
            transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print(f"Transcription completed. Transcript available at: {transcript_file_uri}")
            return await self.parse_transcript_uri(transcript_file_uri)
        else:
            print(f"Transcription job failed: {status['TranscriptionJob']['FailureReason']}")
            return None

    # Parse transcript asynchronously
    async def parse_transcript_uri(self, transcript_file_uri):
        print(f"Parsing transcript URI: {transcript_file_uri}")
        try:
            response = await asyncio.get_event_loop().run_in_executor(None, requests.get, transcript_file_uri)
            response.raise_for_status()

            transcript_data = response.json()
            transcript_text = transcript_data['results']['transcripts'][0]['transcript']
            print(f"Transcript text: {transcript_text}")
            return transcript_text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
        except KeyError as e:
            print(f"Key error: {e} not found in the transcript data.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Store audio in S3 asynchronously
    async def store_audio_as_uri(self, audio_file_path):
        file_name = os.path.basename(audio_file_path)
        s3_key = f"audio/{file_name}"

        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(
                None,
                lambda: self.s3_client.upload_file(str(audio_file_path), self.bucket_name, s3_key)
            )
            print(f"Audio file {file_name} uploaded to S3 at: s3://{self.bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Error uploading audio file to S3: {e}")

        return f"s3://{self.bucket_name}/{s3_key}"
