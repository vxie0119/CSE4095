import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('hw09-image-metadata')

def db_writer(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        size = record['s3']['object']['size']
        # You would get the last modified date from the event or the S3 object metadata
        last_modified = datetime.now().isoformat()  
        write_to_db(bucket, key, size, last_modified)

def write_to_db(bucket, key, size, last_modified):
    response = table.put_item(
        Item={
            'Bucket': bucket,
            'Key': key,
            'Size': size,
            'LastModified': last_modified
        }
    )
    print(response)  # This will log to AWS CloudWatch
