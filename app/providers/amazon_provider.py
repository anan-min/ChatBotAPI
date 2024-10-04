import boto3 
import time 
from urllib.parse import urlparse
import json 
from dotenv import load_dotenv
import os 
import requests

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class AmazonProvider:
    def __init__(self, bucket_name):

        self.stt = boto3.client('transcribe', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='ap-southeast-2')
        self.polly = boto3.client('polly', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='ap-southeast-2')
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')



    def transcribe_audio_file(self, audio_file_path):
        job_name = "transcribe-job-" + str(int(time.time() * 1000))
        job_uri = self.store_audio_as_uri(audio_file_path)
        print(f"Started transcription job: {job_name} for URI: {job_uri}")

        self.stt.start_transcription_job(
            TranscriptionJobName=job_name, 
            Media={'MediaFileUri': job_uri},
            MediaFormat='wav', 
            LanguageCode='th-TH'
        )

        
        return self.process_response(job_name, 5)
    



    def process_response(self, job_name, check_interval):
        print(f"Checking transcription status for job: {job_name}")
        while True:
            status = self.stt.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                print(f"Transcription job {job_name} status: {status['TranscriptionJob']['TranscriptionJobStatus']}")
                break
            time.sleep(check_interval)  

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print(f"Transcription completed. Transcript available at: {transcript_file_uri}")
            return self.parse_transcript_uri(transcript_file_uri)
        else:
            print(f"Transcription job failed: {status['TranscriptionJob']['FailureReason']}")
            return None



    def parse_transcript_uri(self, transcript_file_uri):
        print(f"Parsing transcript URI: {transcript_file_uri}")
        parsed_uri = urlparse(transcript_file_uri)
        key = parsed_uri.path.lstrip('/')

        try:
            response = requests.get(transcript_file_uri)
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

    
    
    def store_audio_as_uri(self, audio_file_path):
        file_name = os.path.basename(audio_file_path)
        s3_key = f"audio/{file_name}"
        
        try:
            self.s3_client.upload_file(str(audio_file_path), self.bucket_name, s3_key)
            print(f"Audio file {file_name} uploaded to S3 at: s3://{self.bucket_name}/{s3_key}")
        except:
            pass

        return f"s3://{self.bucket_name}/{s3_key}"

    
    
    
if __name__ == "__main__":
    bucket_name = "speech-to-text-storage"  
    s3_helper = AmazonProvider(bucket_name)

