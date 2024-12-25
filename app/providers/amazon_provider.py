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

        self.stt = boto3.client('transcribe', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='ap-southeast-2')
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')



    async def transcribe_audio_file(self, audio_file_path):
        job_name = "transcribe-job-" + str(int(time.time() * 1000))
        job_uri = self.store_audio_as_uri(audio_file_path)

        
        self.stt.start_transcription_job(
            TranscriptionJobName=job_name, 
            Media={'MediaFileUri': job_uri},
            MediaFormat='wav', 
            LanguageCode='th-TH'
        )

        return await self.process_response(job_name, 5)

    



    async def process_response(self, job_name, check_interval):
        while True:
            status = self.stt.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            await asyncio.sleep(check_interval)  # ใช้ asyncio.sleep แทน time.sleep เพื่อรองรับ async

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return self.parse_transcript_uri(transcript_file_uri)
        else:
            return None



    def parse_transcript_uri(self, transcript_file_uri):
        parsed_uri = urlparse(transcript_file_uri)
        key = parsed_uri.path.lstrip('/')

        try:
            response = requests.get(transcript_file_uri)
            response.raise_for_status()  

            transcript_data = response.json()  
            transcript_text = transcript_data['results']['transcripts'][0]['transcript']
            return transcript_text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
        except KeyError as e:
            print(f"Key error: {e} not found in the transcript data.")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    
    def store_audio_as_uri(self, audio_file_path):
        file_name = os.path.basename(audio_file_path)
        s3_key = f"audio/{file_name}"
        
        try:
            self.s3_client.upload_file(str(audio_file_path), self.bucket_name, s3_key)
        except:
            pass

        return f"s3://{self.bucket_name}/{s3_key}"

    
    
    
if __name__ == "__main__":
    bucket_name = "speech-to-text-storage"  
    s3_helper = AmazonProvider(bucket_name)

