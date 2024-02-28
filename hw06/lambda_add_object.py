import logging
import base64
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Parse body content from event
        body = json.loads(event['body-json'])
        file_name = body['file_name']
        file_content = base64.b64decode(body['file_content'])

        # Extract bucket name
        bucket_name = event['params']['path']['bucket-name']

        # Upload file
        s3_response = s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)   
        logger.info('S3 Response: {}'.format(s3_response))
        response_body = 'Your file has been uploaded'


    except Exception as e:
        logger.error("Error uploading file: {}".format(e))
        response_body = 'Error in file upload: {}'.format(e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': response_body})
        }
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true'
        },
        'body': json.dumps({'message': response_body})
    }
