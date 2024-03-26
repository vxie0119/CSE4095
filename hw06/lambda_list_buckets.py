import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()

    # Names
    names = [bucket['Name'] for bucket in buckets['Buckets']]

    return {
        'statusCode': 200,
        'body': json.dumps(names)
    }
