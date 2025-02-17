import unittest
import os
import tempfile
import boto3
from moto import mock_aws
from application import list_buckets, upload, list_contents, get_file

class TestS3Client(unittest.TestCase):

    @mock_aws
    def test_list_buckets_empty(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        buckets = list_buckets(s3)
        self.assertEqual(buckets, [])

    @mock_aws
    def test_list_buckets_with_buckets(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        buckets = list_buckets(s3)
        self.assertEqual(buckets, ['test-bucket'])

    @mock_aws
    def test_upload_file(self):
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
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, 'test_file.txt')
            with open(file_path, 'w') as f:
                f.write('Test Content')

            upload(s3, tmp_dir, 'test-bucket')

            result = s3.list_objects(Bucket='test-bucket')['Contents']
            self.assertEqual(len(result), 1)
            self.assertIn('test_file.txt', result[0]['Key'])

    @mock_aws
    def test_list_contents_empty_bucket(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        contents = list_contents(s3, 'test-bucket')
        self.assertEqual(contents, [])

    @mock_aws
    def test_list_contents_with_objects(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test_file.txt', Body='Test Content')
        contents = list_contents(s3, 'test-bucket')
        self.assertEqual(contents, ['test_file.txt'])

    @mock_aws
    def test_get_file(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='test-bucket')
        s3.put_object(Bucket='test-bucket', Key='test_file.txt', Body='Test Content')

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, 'test_file.txt')
            get_file(s3, 'test-bucket', 'test_file.txt', file_path)

            with open(file_path, 'r') as f:
                content = f.read()
            self.assertEqual(content, 'Test Content')


if __name__ == '__main__':
    unittest.main()

