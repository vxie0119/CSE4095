from main import app
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main(client):
    # Tests the main route
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.content_type

def test_success_route(client):
    # Tests the success route
    test_file = (bytes("file content", 'utf-8'), 'test.txt')
    response = client.post('/success', data={'file': test_file}, content_type='multipart/form-data')
    assert response.status_code == 200
    assert 'Acknowledgement.html' in response.data.decode()

def test_file_list(client):
    # Tests file_list route
    response = client.get('/file_list')
    assert response.status_code == 200
    assert 'file_list.html' in response.data.decode()
    assert b'File Name' in response.data
    assert b'Size (megabytes)' in response.data
    assert b'Modified Date (Year/MM/DD)' in response.data


    
