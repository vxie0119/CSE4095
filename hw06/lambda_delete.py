import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    s3 = boto3.client('s3')
    bucket = event['bucket']
    file_name = event['file_name']

    # Delete the object from the bucket
    s3.delete_object(Bucket=bucket, Key=file_name)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'{file_name} deleted from {bucket}'})
    }
