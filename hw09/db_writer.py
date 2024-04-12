import boto3
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('hw09-image-metadata')

def lambda_handler(event, context):
    for record in event['Records']:
        try:
            sns = json.loads(record['body'])
            s3_message = json.loads(sns['Message'])

            s3_record = s3_message['Records'][0]
            file_name = s3_record['s3']['object']['key']
            size = s3_record['s3']['object']['size']
            event_time = s3_record['eventTime']
            date = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")

            item = {
                'FileName': file_name,
                'Date': date,
                'Size': size
            }

            response = table.put_item(Item=item)
            print(f"Item written to DynamoDB: {item}")

        except Exception as e:
            print(f"Error processing record: {record}, error: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('S3 event processed and data is uploaded to DynamoDB.')
    }
