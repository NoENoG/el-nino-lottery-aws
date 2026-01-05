import json
import boto3 # type: ignore
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(table_name)

cors_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
}

def lambda_handler(event, context):
    try:
        print(f"DEBUG: Received event: {event}")

        # 1. Extract ticket number from query parameters or POST body
        user_ticket = None
        
        if event.get('queryStringParameters') and 'number' in event['queryStringParameters']:
            user_ticket = event['queryStringParameters']['number']
        
        elif event.get('body'):
            try:
                body = json.loads(event.get('body'))
                user_ticket = body.get('ticket') or body.get('number')
            except:
                pass

        # 2. Validation
        if not user_ticket:
             return { 
                 'statusCode': 400, 
                 'headers': cors_headers, 
                 'body': json.dumps({'error': 'No ticket number provided. Use ?number=12345'}) 
             }

        print(f"Checking ticket: {user_ticket}")

        # 3. Query DynamoDB
        response = table.get_item(
            Key={
                'DrawDate': user_ticket 
            }
        )

        # 4. Handle Response
        if 'Item' in response:
            item = response['Item']
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({
                    'result': 'WIN',
                    'prize': item.get('Prize', '€0'),
                    'category': item.get('Category', 'Winner')
                })
            }
        else:
            return {
                'statusCode': 200,
                'headers': cors_headers,
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
            'headers': cors_headers,
            'body': json.dumps({'error': str(e)})
        }