import pytest
import json
from http_utils import *


# Define constants for the test
API_URL = "https://qppgh6p2uk.execute-api.us-east-1.amazonaws.com/prod"
BUCKET = "hw06.s3"
FILE_NAME = "giants.png"
FILE_PATH = "/Downloads/giants.png"  

# Replace these with the actual endpoints or the mock endpoints if you are mocking
LIST_BUCKET_URL = f"{API_URL}/list"
LIST_OBJECTS_URL = f"{API_URL}/{BUCKET}"
POST_OBJECT_URL = f"{API_URL}/{BUCKET}"
DELETE_OBJECT_URL = f"{API_URL}/{BUCKET}/{FILE_NAME}"

# This can be used if your Lambda function is expected to return these responses
SUCCESS_RESPONSE = {"statusCode": 200, "body": json.dumps({"message": "success"})}
FAILURE_RESPONSE = {"statusCode": 400, "body": json.dumps({"message": "failure"})}

# Test GET request to list objects
def test_list_objects():
    expected_data = create_post_data_for_list_objects(BUCKET, FILE_NAME)
    response = get(LIST_OBJECTS_URL)
    # Assert statements should compare the response to expected values
    assert response == SUCCESS_RESPONSE