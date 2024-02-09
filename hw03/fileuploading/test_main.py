import pytest
import os
from io import BytesIO
from main import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_main_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type

def test_success_route_get_method(client):
    response = client.get('/success')
    assert response.status_code == 405  # 405 Method Not Allowed

def test_success_route_post_method(client):
    data = {
        'file': (BytesIO(b'my file contents'), 'test.txt')
    }
    response = client.post('/success', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'File uploaded successfully' in response.data.decode()

def test_file_list_route(client):
    response = client.get('/file_list')
    assert response.status_code == 200
    assert 'text/html' in response.content_type


def test_file_upload_and_listing(client):
    # Upload a file
    data = {
        'file': (BytesIO(b'test file content'), 'test_upload.jpg')
    }
    client.post('/success', data=data, content_type='multipart/form-data')

    # Check if the file appears in the file list
    response = client.get('/file_list')
    assert response.status_code == 200
    assert 'test_upload.jpg' in response.data.decode()

def test_non_image_file_filter(client):
    # Assuming your application should only list image files
    # Upload a non-image file
    data = {
        'file': (BytesIO(b'non-image content'), 'test.txt')
    }
    client.post('/success', data=data, content_type='multipart/form-data')

    # Checks if the non-image file is not listed
    response = client.get('/file_list')
    assert response.status_code == 200
    assert 'test.txt' not in response.data.decode()



    
