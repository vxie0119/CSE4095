import json
import boto3


dynamodb = boto3.resource('dynamodb')
table_name = 'Players'

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)

    try:
        # parse JSON data from event body
        body = json.loads(event['body'])

        # put item into db
        response = table.put_item(
            Item={
                'name': body['name'],
                'team': body['team'],
                'number': body['number']
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Player data added successfully.')
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error writing to the DynamoDB table.')
        }