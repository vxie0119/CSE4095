import json
import base64
import boto3

def lambda_handler(event, context):
    print(event)
    bucket_name = event['body-json']['bucket']
    file_name = event['body-json']['file_name']
    
    print("bucket", bucket_name, "file", file_name)
    file_content = base64.b64decode(event['body-json']['body'])
    
    s3 = boto3.client('s3')
    
    # Puts objects into bucket
    s3_response = s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
    print('S3 Response: {}'.format(s3_response))
    return {
        'statusCode': 200,
        'body': json.dumps(s3_response)
    }