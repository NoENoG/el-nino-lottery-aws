import json
import boto3 # type: ignore
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # 1. Extract Ticket from Request
        body = json.loads(event.get('body', '{}'))
        user_ticket = body.get('ticket')

        if not user_ticket:
             return { 'statusCode': 400, 'body': json.dumps({'error': 'No ticket provided'}) }

        print(f"Checking ticket: {user_ticket}")

        # 2. Query DynamoDB Table
        response = table.get_item(
            Key={
                'DrawDate': user_ticket 
            }
        )

        if 'Item' in response:
            # MATCH FOUND
            item = response['Item']
            return {
                'statusCode': 200,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({
                    'result': 'WIN',
                    'prize': item.get('Prize', '€0'),
                    'category': item.get('Category', 'Winner')
                })
            }
        else:
            # NO MATCH
            return {
                'statusCode': 200,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({
                    'result': 'LOSS',
                    'prize': '0',
                    'category': 'Better luck next time'
                })
            }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }# force update
