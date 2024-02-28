import json
import boto3
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    bucket = event['pathParameters']['bucket-name']
    body = json.loads(event['body'])

    object_name = unquote_plus(body['name'])
    object_content = body['content']

    # Add the object to the bucket
    s3.put_object(Bucket=bucket, Key=object_name, Body=object_content)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'{object_name} added to {bucket}'})
    }
