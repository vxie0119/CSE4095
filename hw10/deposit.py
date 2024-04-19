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

    # input has to be compatible
    deposit_amount = Decimal(str(deposit_amount))

    try:
        response = table.get_item(
            Key={
                'account': account_number
            }
        )

        # account check
        if 'Item' not in response:
            return {"error": 'Account not found'}
        
        current_bal = response['Item']['balance']

        new_bal = current_bal + deposit_amount

        # update item
        result = table.update_item(
            Key={
                'account': account_number
            },
            UpdateExpression='SET balance = :val',
            ExpressionAttributeValues={
                ':val': new_bal
            },
            ReturnValues='UPDATED_NEW'
        )

        # return the new balance
        return {
            'account': account_number,
            'new_balance': new_bal
        }
    except Exception as e:
        print(e)
        return {'error': 'Could not update the account balance'}