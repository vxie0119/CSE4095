from PIL import Image
import boto3
from boto3.s3.transfer import TransferConfig
from io import BytesIO
import json

s3_res = boto3.resource('s3')
CONFIG = TransferConfig(multipart_threshold=1024 * 10,
                        multipart_chunksize=1024 * 10,
                        use_threads=True)

def lambda_handler(event=None, context=None):
    #print(f'Received event: {json.dumps(event)}')
    #print(event)
    #if 'Records' not in event:
        #print('Error: No Records key in event object. Event does not contain expected structure.')
        #return {'statusCode': 400, 'body': json.dumps('Error: No Records key in event.')}

    body_json = json.loads(event['Records'][0]['body'])
    message_json = json.loads(body_json['Message'])

    s3_info = message_json['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key = s3_info['object']['key']
            
    print(f'Origin Bucket: {bucket_name}')
    print(f'File Key: {key}. Processing.')

    original_image_response = s3_res.Object(Bucket=bucket_name, Key=key)
    original_image = original_image_response.get()['Body'].read()
            
    with Image.open(BytesIO(original_image)) as img:
        print(f'Before image size: {img}')
        img.thumbnail((300, 300))
        print(f'After image size: {img}')

        print('Thumbnail Generated')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        print('Uploading')
        target_bucket = 'hw09-thumbnails-vx' 
        thumbnail_key = f'thumbnails/{key}'
        s3_res.upload_fileobj(buffer, target_bucket, thumbnail_key)
        print('Successful upload')

    print(f'Operation Completed for: {key}')

    return {
        'statusCode': 200,
        'body': json.dumps('Thumbnail generation and upload complete')
    }