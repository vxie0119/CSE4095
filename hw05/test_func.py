import boto3
import pytest
import time

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('hw05-db')  # Replace with your DynamoDB table name

def upload_to_s3(bucket, key, content):
    s3_client.put_object(Bucket=bucket, Key=key, Body=content)

def get_item_from_dynamodb(file_name, arn):
    response = table.get_item(Key={'file_name': file_name, 'ARN': arn})
    return response.get('Item', None)

@pytest.mark.parametrize("file_name, content", [
    ("testfile1.txt", "This is a test file."),
    ("testfile2.txt", "Another test file content.")
])
def test_upload_trigger_lambda(file_name, content):
    bucket_name = 'your-s3-bucket'  # Replace with your S3 bucket name
    arn = f'arn:aws:s3:::{bucket_name}/{file_name}'

    # Upload to S3
    upload_to_s3(bucket_name, file_name, content)

    # Wait for Lambda to process the file
    time.sleep(10)  # Adjust time as needed for your Lambda function

    # Verify DynamoDB contents
    item = get_item_from_dynamodb(file_name, arn)
    assert item is not None
    assert item['file_name'] == file_name
    assert item['ARN'] == arn
    assert 'file_size' in str(len(content))
    assert 'upload_date' in item
    assert 'eTag' in item

