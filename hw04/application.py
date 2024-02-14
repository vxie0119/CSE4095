import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

def main_menu():
    s3 = boto3.client('s3')
    while True:
        print("\nMain Menu:")
        print("1. List all buckets")
        print("2. Backup files to a bucket")
        print("3. List all objects in bucket")
        print("4. Download object from selected bucket")
        print("5. Exit")
        choice = input("Enter your choice:")

        if choice == '1':
            list_buckets()
        elif choice == '2':
            local = input('Enter the path to the local folder: ')
            bucket = input('Enter the bucket name: ')
            upload(local, bucket)
        elif choice == '3':
            bucket = input('Enter the bucket name: ')
            try:
                contents = list_contents(bucket)
                for item in contents:
                    print(item)
            except ClientError as e:
                print(f"An error occured: {e}")
        elif choice == '4':
            bucket = input('Enter the bucket name: ')
            file = input('Enter the file name: ')
            get_file(bucket, file)
        elif choice == '5':
            break
        else:
            print('Invalid choice.')
         
def upload(local, bucket):
    s3_client = boto3.client('s3')
    for subdir, dirs, files in os.walk(local):
        for file in files:
            full_path = os.path.join(subdir, file)
            key = os.path.relpath(full_path, local)
            try:
                with open(full_path, 'rb') as data:
                    s3_client.upload_fileobj(data, bucket, key)
                print(f"Uploaded {full_path} to {bucket}/{key}")
            except FileNotFoundError:
                print(f"File not found: {full_path}")
            except ClientError as e:
                print(f"An error occurred uploading {full_path}: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
     
def list_contents(bucket):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket)
    if 'Contents' in response:
        return [item['Key'] for item in response['Contents']]
    else:
        return []
 
def get_file(bucket, file):
    try:
        s3_client = boto3.client('s3')
        download_path = os.path.join(os.getcwd(), file)
        with open(file, 'wb') as data:
            s3_client.download_fileobj(bucket, file, data)
        print(f"File '{file}' downloaded successfully.")
    except ClientError as e:
        print(f"An error occurred: {e}")


def list_buckets():
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        print("Bucket List: ")
        for bucket in response['Buckets']:
            print(bucket['Name'])
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    main_menu()