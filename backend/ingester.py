import boto3 # type: ignore
import os
import json
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('DYNAMODB_TABLE')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("🤖 Mock Ingester Started...")
    
    # Mock Data: Ticket 12345 wins 200k
    mock_data = {
        'DrawDate': '2026-01-06',
        'Jackpot': '12345',
        'Prizes': {
            '12345': 200000,
            '99999': 20,
        },
        'LastUpdated': datetime.now().isoformat()
    }

    try:
        table.put_item(Item=mock_data)
        print(f"✅ Success! Wrote mock data to {TABLE_NAME}")
        return {'statusCode': 200, 'body': json.dumps('Mock Data Ingested')}
    except Exception as e:
        print(f"❌ Error writing to DB: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Error: {str(e)}")}