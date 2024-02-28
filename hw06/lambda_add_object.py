import json
import base64
import boto3

def lambda_hander(event, context):
    s3 = boto3.client('s3')

    get_file = event['content']
    decode_content = base64.b64decode(get_file)
    bucket = event['bucket']['bucket-name']
    object = event['pathParameters']['object-name']

    s3_upload = s3.put_object(Bucket=bucket, Key=object, Body=decode_content)

    return {
        'statusCode': 200,
        'body': json.dumps('Object is uploaded successfully.')
    }