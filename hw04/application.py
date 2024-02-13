import boto3
import os

def get_file(bucket, file, s3_client):
    with open(file, 'wb') as data:
        s3_client.download_fileobj(bucket, file, data)