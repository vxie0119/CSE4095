"""Importing Modules"""
import unittest
import os
import tempfile
import boto3
from moto import mock_aws
from application import upload, list_contents, get_file, list_buckets, \
                        generate_presigned_url, list_object_versions, delete_object

class TestS3Client(unittest.TestCase):
    """Testing S3 Client"""
    @mock_aws
    def test_list_buckets_empty(self):
        """Testing if the list of buckets is empty"""
        s3 = boto3.client('s3', region_name='us-east-1')
        buckets = list_buckets(s3)
        self.assertEqual(buckets, [])

    @mock_aws
    def test_list_buckets_with_buckets(self):
        """Testing list_buckets function"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        buckets = list_buckets(s3)
        self.assertEqual(buckets, ['test-bucket'])

    @mock_aws
    def test_upload_file(self):
        """Testing upload function"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'Hello World')
            tmp_path = tmp.name

        upload(s3, tmp_path, 'test-bucket')

        result = s3.list_objects(Bucket='test-bucket')['Contents']
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Key'], os.path.basename(tmp_path))

        os.remove(tmp_path)

    @mock_aws
    def test_upload_directory(self):
        """Testing upload directory"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, 'test_file.txt')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('Test Content')

            upload(s3, tmp_dir, 'test-bucket')

            result = s3.list_objects(Bucket='test-bucket')['Contents']
            self.assertEqual(len(result), 1)
            self.assertIn('test_file.txt', result[0]['Key'])

    @mock_aws
    def test_list_contents_empty_bucket(self):
        """Testing to see if contents is empty"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        contents = list_contents(s3, 'test-bucket', '')
        self.assertEqual(contents, [])

    @mock_aws
    def test_list_contents_with_objects(self):
        """Testing list_contents function"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test_file.txt', Body='Test Content')
        contents = list_contents(s3, 'test-bucket', '')
        self.assertEqual(contents, ['test_file.txt'])

    @mock_aws
    def test_get_file(self):
        """Testing get_file function"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test_file.txt', Body='Test Content')

        with tempfile.TemporaryDirectory() as tmp_dir:
            # Change the current working directory to the temporary directory
            os.chdir(tmp_dir)

            # Call get_file, which now saves the file in the current working directory
            get_file(s3, 'test-bucket', 'test_file.txt', '')

            # Check if the file was downloaded correctly
            with open('test_file.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertEqual(content, 'Test Content')

    @mock_aws
    def test_generate_presigned_url(self):
        """Testing presigned URL"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test-file.txt', Body='Test content')

        url = generate_presigned_url(s3, 'test-bucket', 'test-file.txt')
        self.assertIn('test-bucket', url)
        self.assertIn('test-file.txt', url)

    @mock_aws
    def test_list_object_versions(self):
        """Testing object versions"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test-file.txt', Body='Test content')

        versions = list_object_versions(s3, 'test-bucket', 'test-file.txt')
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0]['Key'], 'test-file.txt')

    @mock_aws
    def test_delete_object(self):
        """Testing deletion of object"""
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test-file.txt', Body='Test content')

        delete_object(s3, 'test-bucket', 'test-file.txt')
        response = s3.list_objects(Bucket='test-bucket')
        self.assertNotIn('Contents', response)

if __name__ == '__main__':
    unittest.main()
