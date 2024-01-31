def lambda_handler(event, context):
    # Print the event to the logs of the Lambda function
    print(f"Received event: {event}")

    # Return a simple message
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
