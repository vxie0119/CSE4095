import boto3
import os
from PIL import Image
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
