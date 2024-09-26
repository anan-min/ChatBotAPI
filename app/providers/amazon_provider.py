import boto3 
import time 
import urllib
import json 
from dotenv import load_dotenv
import os 

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


class AmazonProvider:
    def __init__(self):
        self.stt = boto3.client('transcribe', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')

    def transcribe_audio_file(self, audio_file_path):
        job_name = "transcribe-job-" + str(int(time.time() * 1000))
        job_uri = self.store_audio_as_uri(audio_file_path)

        self.stt.start_transcription_job (
                TranscriptionJobName=job_name, 
                ia={'MediaFileUri': job_uri},
                MediaFormat='wav', 
                LanguageCode='en-US'
        )

        return self.process_reponse(job_name, 5) 


    def speech_synthesis(self, text):
        pass 


    def query_text_file(self, text):
        pass



    def process_reponse(self, job_name, check_interval):
        while True:
            status = self.stt.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            time.sleep(check_interval)  # Wait before polling again to avoid hitting rate limits

        # Handle the completed transcription
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
 

        return self.parse_transcript_uri(transcript_file_uri)
    


    def parse_transcript_uri(self, transcript_file_uri):
        parsed_uri = urllib.urlparse(transcript_file_uri)
        bucket_name = parsed_uri.netloc
        key = parsed_uri.path.lstrip('/')

        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=key)
        
        transcript_json = response['Body'].read().decode('utf-8')
        transcript_data = json.loads(transcript_json)

        transcript_text = transcript_data['results']['transcripts'][0]['transcript']
        return transcript_text


    def store_audio_as_uri(self, audio_file_path):
        file_name = os.path.basename(audio_file_path)
        s3_key = f"audio/{file_name}"
        self.s3_client.upload_file(audio_file_path, self.bucket_name, s3_key)
        return f"s3://{self.bucket_name}/{s3_key}"

