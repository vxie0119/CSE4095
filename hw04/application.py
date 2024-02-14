"""Importing Modules"""
import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
def main_menu():
    """Main Menu function"""
    s3 = boto3.client('s3')
    while True:
        print("\nMain Menu:")
        print("1. List all buckets")
        print("2. Backup files to a bucket")
        print("3. List all objects in bucket")
        print("4. Download object from selected bucket")
        print("5. Generate a pre-signed URL for an object")
        print("6. List all version information for an object")
        print("7. Delete an object from a bucket")
        print("8. Exit")
        choice = input("Enter your choice:")

        if choice == '1':
            list_buckets(s3)
        elif choice == '2':
            local = input('Enter the path to the local folder: ')
            bucket = input('Enter the bucket name: ')
            upload(s3, local, bucket)
        elif choice == '3':
            bucket = input('Enter the bucket name: ')
            try:
                contents = list_contents(s3, bucket, '')
                for item in contents:
                    print(item)
            except ClientError as e:
                print(f"An error occured: {e}")
        elif choice == '4':
            bucket = input('Enter the bucket name: ')
            file = input('Enter the file name: ')
            get_file(s3, bucket, file, '')
        elif choice == '5':
            bucket = input('Enter the bucket name: ')
            file = input('Enter the file name: ')
            url = generate_presigned_url(s3, bucket, file)
            if url:
                print("Pre-signed URL: ", url)
        elif choice == '6':
            bucket = input('Enter the bucket name: ')
            file = input('Enter the file name: ')
            versions = list_object_versions(s3, bucket, file)
            for version in versions:
                print(version)
        elif choice == '7':
            bucket = input('Enter the bucket name: ')
            file = input('Enter the file name: ')
            delete_object(s3, bucket, file)
        elif choice == '8':
            break
        else:
            print('Invalid choice.')
            
def upload(s3, local_path, bucket):
    """Upload function"""
    local_path = os.path.expanduser(local_path)  # Expand the ~ symbol

    # Check if the path is a directory
    if os.path.isdir(local_path):
        # If it's a directory, upload each file
        for subdir, _, files in os.walk(local_path):
            for file in files:
                full_path = os.path.join(subdir, file)
                key = os.path.relpath(full_path, local_path)
                try:
                    s3.upload_file(full_path, bucket, key)
                    print(f"Uploaded {file} to {bucket}/{key}")
                except ClientError as e:
                    print(f"An error occurred: {e}")
    elif os.path.isfile(local_path):
        # If it's a file, just upload the file
        try:
            file_name = os.path.basename(local_path)
            s3.upload_file(local_path, bucket, file_name)
            print(f"Uploaded {file_name} to {bucket}/{file_name}")
        except ClientError as e:
            print(f"An error occurred: {e}")
    else:
        print(f"The provided path does not exist: {local_path}")
def list_contents(s3, bucket, folder_name):
    """Lists the contents in a specific folder within a bucket."""
    response = s3.list_objects_v2(Bucket=bucket, Prefix=folder_name)
    if 'Contents' in response:
        return [item['Key'] for item in response['Contents'] if item['Key'].startswith(folder_name)]
    return []
def get_file(s3, bucket, file, folder_name):
    """Download a file from a specific folder within a bucket."""
    try:
        file_key = os.path.join(folder_name, file) if folder_name else file
        local_path = os.path.join(os.getcwd(), file)
        s3.download_file(bucket, file_key, local_path)
        print(f"File '{file}' downloaded successfully.")
    except ClientError as e:
        print(f"An error occurred: {e}")
def list_buckets(s3):
    """Listing all buckets"""
    try:
        response = s3.list_buckets()
        print("Bucket List: ")
        bucket_names = [bucket['Name'] for bucket in response.get('Buckets', [])]
        for name in bucket_names:
            print(name)
        return bucket_names
    except NoCredentialsError:
        print("Credentials not available.")
        return []
    except ClientError as e:
        print(f"An error occurred: {e}")
        return []

def generate_presigned_url(s3, bucket_name, object_name, expiration=604800):
    """Generate a pre-signed URL to share an S3 object"""
    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name, 'Key': object_name},
                                             ExpiresIn=expiration)
    except ClientError as e:
        print(f"Error generating pre-signed URL: {e}")
        return None

    return response

def list_object_versions(s3, bucket_name, object_name):
    """List all versions of an object in an S3 bucket"""
    try:
        versions = s3.list_object_versions(Bucket=bucket_name, Prefix=object_name)
        return versions.get('Versions', [])
    except ClientError as e:
        print(f"Error retrieving object versions: {e}")
        return []

def delete_object(s3, bucket_name, object_name):
    """Delete an object from an S3 bucket"""
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"Object '{object_name}' deleted successfully from bucket '{bucket_name}'.")
    except ClientError as e:
        print(f"Error deleting object: {e}")

if __name__ == "__main__":
    main_menu()
