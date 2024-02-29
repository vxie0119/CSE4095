import pytest
import json
from http_utils import *


# Define constants for the test
API_URL = "https://qppgh6p2uk.execute-api.us-east-1.amazonaws.com/prod"
BUCKET = "hw06.s3"
FILE_NAME = "giants.png"
FILE_PATH = "./hw06/giants.png"  

# Replace these with the actual endpoints or the mock endpoints if you are mocking
LIST_BUCKET_URL = f"{API_URL}/list"
LIST_OBJECTS_URL = f"{API_URL}/{BUCKET}"
POST_OBJECT_URL = f"{API_URL}/{BUCKET}"
DELETE_OBJECT_URL = f"{API_URL}/{BUCKET}/{FILE_NAME}"



def test_list_buckets():
    response = get(LIST_BUCKET_URL)
    assert response['statusCode'] == 200

def test_list_objects():
    response = get(LIST_OBJECTS_URL)
    assert response['statusCode'] == 200

def test_add_object():
    file_content = read_file_into_base64_string(FILE_PATH)
    post_data = create_post_data_for_post_object(BUCKET, FILE_NAME, file_content)
    response = post(POST_OBJECT_URL, post_data)
    assert response['statusCode'] == 200

def test_delete_object():
    data = create_data_for_del_object(BUCKET, FILE_NAME)
    response = delete(DELETE_OBJECT_URL, data)
    assert response['statusCode'] == 200

if __name__ == "__main__":
    pytest.main()