import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

# Initialize the boto3 client for DynamoDB
dynamodb = boto3.resource('dynamodb')

# Specify your DynamoDB table name
table = dynamodb.Table('hw05-db')  # Replace with your actual table name

def lambda_handler(event, context)
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        file_size = record['s3']['object'].get('size', 0)
        eTag = record['s3']['object'].get('eTag')
        bucket_arn = f"arn:aws:s3:::{bucket_name}/{object_key}"
        upload_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Define the key for the DynamoDB get_item request
        # Include both the partition key (file_name) and the sort key (ARN)
        dynamo_key = {
            'file_name': object_key,
            'ARN': bucket_arn
        }

        try:
            # Attempt to get the existing item from DynamoDB table
            response = table.get_item(Key=dynamo_key)
            if 'Item' in response:
                # If the item exists, update it
                table.update_item(
                    Key=dynamo_key,
                    UpdateExpression="set file_size = :fs, upload_date = :ud, eTag = :et",
                    ExpressionAttributeValues={
                        ':fs': str(file_size),
                        ':ud': upload_date,
                        ':et': eTag
                    }
                )
                print(f"Updated existing item: {object_key} with ARN {bucket_arn}.")
            else:
                # If the item does not exist, insert it
                table.put_item(
                    Item={
                        'file_name': object_key,
                        'ARN': bucket_arn,  # The sort key
                        'upload_date': upload_date,
                        'file_size': str(file_size),
                        'eTag': eTag
                    }
                )
                print(f"Inserted new item: {object_key} with ARN {bucket_arn}.")
        except ClientError as e:
            print(f"Error: {e.response['Error']['Message']}")
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed S3 event.')
    }
