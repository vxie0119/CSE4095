import boto3
import os

def list_contents(bucket, s3_client):
    contents = []
    for item in s3_client.list_objects_v2(Bucket=bucket)['Contents']:
        contents.append(item['Key'])
    return contents