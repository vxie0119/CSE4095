import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.client('s3')
    bucket = event['pathParameters']['bucket-name']
    object = event['pathParameters']['object-name']

    # Delete the object from the bucket
    s3.delete_object(Bucket=bucket, Key=object)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'{object} deleted from {bucket}'})
    }
