import logging
import base64
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = event['bucket']
    file_name = event['file_name']
    
    # The file content is expected to be base64-encoded in the body
    file_content = base64.b64decode(event['body'])

    try:
        s3_response = s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_content)   
        logger.info('S3 Response: {}'.format(s3_response))
        response_body = 'Your file has been uploaded'


    except Exception as e:
        logger.error("Error uploading file: {}".format(e))
        response_body = 'Error in fiel upload'

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true'
        },
        'body': json.dumps({'message': response_body})
    }
