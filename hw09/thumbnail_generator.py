import boto3
import os
from PIL import Image
import io

s3_client = boto3.client('s3')

def thumbnail_generator(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        image = get_image(bucket, key)
        thumbnail = create_thumbnail(image)
        s3_save(bucket, key, thumbnail)

def get_image(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read()
    image = Image.open(io.BytesIO(content))
    return image

def create_thumbnail(image):
    thumbnail_size = (128, 128)
    image.thumbnail(thumbnail_size)
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)
    return buffer

def s3_save(bucket, key, thumbnail):
    thumbnail_key = 'thumbnails/' + os.path.basename(key)
    s3_client.put_object(Bucket=bucket, Key=thumbnail_key, Body=thumbnail)