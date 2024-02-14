"""Importing Modules"""
import unittest
from unittest.mock import patch
import application

class TestS3BucketOperations(unittest.TestCase):
    """Testing s3 operations"""
    @patch('application.boto3.client')
    def test_list_buckets(self, mock_boto3_client):
        mock_boto3_client.return_value.list_buckets.return_value = {
        '   Buckets': [{'Name': 'test-bucket'}]
        }
        result = application.list_buckets(mock_boto3_client.return_value)
        mock_boto3_client.return_value.list_buckets.assert_called_once()
        self.assertIn('test-bucket', [b['Name'] for b in result['Buckets']])


    @patch('application.boto3.client')
    def test_upload(self, mock_boto3_client):
        """Testing upload"""
        with patch('application.os.path.isdir') as mock_isdir, \
             patch('application.os.walk') as mock_os_walk:
            mock_isdir.return_value = True
            mock_os_walk.return_value = [('/path/to/dir', ('dir1',), ('file1',))]
            application.upload(mock_boto3_client, '/path/to/dir', 'test-bucket')
            mock_boto3_client.return_value.upload_file.assert_called_with
            ('/path/to/dir/file1', 'test-bucket', 'file1')

    @patch('application.boto3.client')
    def test_list_contents(self, mock_boto3_client):
        mock_boto3_client.return_value.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file1'}, {'Key': 'file2'}]
        }
        result = application.list_contents(mock_boto3_client.return_value, 'test-bucket')
        self.assertEqual(result, ['file1', 'file2'])

    @patch('application.boto3.client')
    def test_get_file(self, mock_boto3_client):
        """Test downloading"""
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            application.get_file(mock_boto3_client, 'test-bucket', 'file1')
            mock_boto3_client.return_value.download_fileobj.assert_called_with
            ('test-bucket', 'file1', mock_file())

if __name__ == '__main__':
    unittest.main()
