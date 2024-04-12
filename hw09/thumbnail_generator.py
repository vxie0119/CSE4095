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

    response = s3_res.meta.client.get_object(Bucket=bucket_name, Key=key)['Body'].read()
            
    with Image.open(BytesIO(response)) as img:
        print(f'Before image size: {img}')
        img.thumbnail((300, 300))
        print(f'After image size: {img}')

        print('Thumbnail Generated')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        print('Uploading')
        response = s3_res.meta.client.upload_fileobj(Fileobj=buffer, Bucket='hw09-thumbnails-vx' , Key=key, Config=CONFIG)
        print('Successful upload')
        print(response)

    print(f'Operation Completed for: {key}')

