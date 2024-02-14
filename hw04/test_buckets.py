import unittest
import boto3
import application  
from moto.s3 import mock_s3  # moto library is used to mock S3

class TestS3BucketOperations(unittest.TestCase):

    @mock_s3
    def setUp(self):
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.s3.create_bucket(Bucket='test-bucket')

    def test_list_buckets(self):
        # Test list_buckets function
        with mock_s3():
            buckets = application.list_buckets(self.s3)
            self.assertIn('test-bucket', [b['Name'] for b in buckets['Buckets']])

    @mock_s3
    def test_upload_file(self):
        # Test upload function with a mock file
        application.upload(self.s3, 'test.txt', 'test-bucket')
        response = self.s3.list_objects_v2(Bucket='test-bucket')
        self.assertIn('test.txt', [obj['Key'] for obj in response.get('Contents', [])])

    @mock_s3
    def test_list_contents(self):
        # Test list_contents function
        self.s3.put_object(Bucket='test-bucket', Key='test.txt', Body='test data')
        contents = application.list_contents(self.s3, 'test-bucket')
        self.assertIn('test.txt', contents)

    @mock_s3
    def test_get_file(self):
        # Test get_file function
        self.s3.put_object(Bucket='test-bucket', Key='test.txt', Body='test data')
        application.get_file(self.s3, 'test-bucket', 'test.txt')


if __name__ == '__main__':
    unittest.main()
