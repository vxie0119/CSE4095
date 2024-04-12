from PIL import Image
import boto3
from boto3.s3.transfer import TransferConfig
from io import BytesIO
import json

s3_res = boto3.resource('s3')
CONFIG = TransferConfig(multipart_threshold=1024 * 10,
                        multipart_chunksize=1024 * 10,
                        use_threads=True)

def lambda_handler(event, context):
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

    original_image = s3_res.Object(bucket_name, key).get()['Body'].read()
            
    with Image.open(BytesIO(original_image)) as img:
        print(f'Before image size: {img.size}')
        img.thumbnail((300, 300))
        print(f'After image size: {img.size}')

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        print('Uploading')
        target_bucket = 'hw09-thumbnails-vx' 
        s3_res.meta.client.upload_fileobj(Fileobj=buffer, Bucket=target_bucket, Key=key, Config=CONFIG)
        print('Successful upload')

    print(f'Operation Completed for: {key}')

    return {
        'statusCode': 200,
        'body': json.dumps('Operation completed')
    }

