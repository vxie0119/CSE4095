import boto3
import csv
from io import StringIO
import json

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'hw05-s3'
    csv_file_name = 'bucket_contents.csv'

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    objects = response.get('Contents', [])

    # Create CSV content
    csv_content = StringIO()
    csv_writer = csv.writer(csv_content)
    csv_writer.writerow(['File Name', 'Last Modified', 'Size'])

    for obj in objects:
        csv_writer.writerow([obj['Key'], obj['LastModified'], obj['Size']])

    # Reset the file pointer to the start
    csv_content.seek(0)

    # Upload the CSV file to the S3 bucket
    s3_client.put_object(Bucket=bucket_name, Key=csv_file_name, Body=csv_content.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps('CSV file created and uploaded to S3.')
    }
