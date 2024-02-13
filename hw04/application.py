import boto3
import os

def upload(local, bucket, s3_client):
    for subdir, dirs, files in os.walk(local):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                s3_client.upload_fileobj(data, bucket, full_path[len(local):])