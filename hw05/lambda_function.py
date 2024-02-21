import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

# Initialize the boto3 client for DynamoDB
dynamodb = boto3.resource('dynamodb')

# Specify your DynamoDB table name
table = dynamodb.Table('hw05-db')  # Replace with your actual table name

def lambda_handler(event, context):
    # Loop through each record in the event
    for record in event['Records']:
        # Get the bucket name and object key from the event
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']
        file_size = record['s3']['object'].get('size', 0)
        eTag = record['s3']['object'].get('eTag')
        
        # Get the S3 object ARN
        bucket_arn = f"arn:aws:s3:::{bucket_name}/{object_key}"
        
        # Get the current time as the upload date
        upload_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # Attempt to insert the file metadata in the DynamoDB table
        try:
            # Check if the item exists
            response = table.get_item(Key={'file_name': object_key})
            if 'Item' in response:
                # Item exists, update it
                table.update_item(
                    Key={'file_name': object_key},
                    UpdateExpression="set file_size = :fs, upload_date = :ud, ARN = :arn, eTag = :et",
                    ExpressionAttributeValues={
                        ':fs': str(file_size),
                        ':ud': upload_date,
                        ':arn': bucket_arn,
                        ':et': eTag
                    }
                )
                print(f"Updated existing item: {object_key}")
            else:
                # Item does not exist, insert it
                table.put_item(
                    Item={
                        'file_name': object_key,
                        'file_size': str(file_size),
                        'upload_date': upload_date,
                        'ARN': bucket_arn,
                        'eTag': eTag
                    }
                )
                print(f"Inserted new item: {object_key}")
        except ClientError as e:
            print(f"Error: {e.response['Error']['Message']}")
            raise e
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed S3 event.')
    }
