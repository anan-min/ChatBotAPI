import boto3
import time
import os

ec2 = boto3.client('ec2')
os.environ['AWS_PROFILE'] = "default"
os.environ['AWS_DEFAULT_REGION'] = "ap-southeast-2"

session = boto3.Session(profile_name='default')  
transcribe = session.client('transcribe', region_name='ap-southeast-2')


def start_transcription_job(job_name, job_uri, language_code):
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3', 
        LanguageCode=language_code
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    return status
