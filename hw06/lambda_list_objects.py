import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    bucket = event['bucket']['bucket-name']

    # List objects within the bucket
    objects = s3.list_objects_v2(Bucket=bucket)
    object_keys =  [obj['Key'] for obj in objects.get('Contents', [])]

    return {
        'statusCode': 200,
        'body': json.dumps(object_keys)
    }
