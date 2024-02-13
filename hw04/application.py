import boto3
import os

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
            for bucket in s3.list_buckets()['Buckets']:
                print(bucket['Name'])
        elif choice == '2':
            local = input('Enter the path to the local folder: ')
            bucket = input('Enter the bucket name: ')
            upload(local, bucket, s3)
        elif choice == '3':
            bucket = input('Enter the bucket name: ')
            contents = list_contents(bucket, s3)
            for item in contents:
                print(item)
        elif choice == '4':
            bucket = input('Enter the bucket name: ')
            file = input('Enter the file name: ')
            get_file(bucket, file, s3)
        elif choice == '5':
            break
        else:
            print('Invalid choice.')
            
def upload(local, bucket, s3_client):
    for subdir, dirs, files in os.walk(local):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                s3_client.upload_fileobj(data, bucket, full_path[len(local):])
                
def list_contents(bucket, s3_client):
    contents = []
    for item in s3_client.list_objects_v2(Bucket=bucket)['Contents']:
        contents.append(item['Key'])
    return contents
 
def get_file(bucket, file, s3_client):
    with open(file, 'wb') as data:
        s3_client.download_fileobj(bucket, file, data)

if __name__ == "__main__":
    main_menu()