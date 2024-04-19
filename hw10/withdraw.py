import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # table name
    table = dynamodb.Table('hw10-account-list')

    # event details
    account_number = event['account']
    deposit_amount = event['amount']