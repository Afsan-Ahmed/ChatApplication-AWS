"""
ChatConnect Lambda Function
Handles new WebSocket connections

Author: Afsan Ahmed P.M.
"""

import json
import boto3
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatConnections')

def lambda_handler(event, context):
    """
    Triggered when a user connects to the WebSocket API.
    Stores the connection ID in DynamoDB to track active users.
    
    Args:
        event: API Gateway WebSocket $connect event
        context: Lambda context object
    
    Returns:
        Success response with 200 status code
    """
    
    # Extract connection ID from the event
    connection_id = event['requestContext']['connectionId']
    
    # Get current timestamp
    timestamp = int(datetime.now().timestamp())
    
    try:
        # Save connection to DynamoDB
        table.put_item(
            Item={
                'connectionId': connection_id,
                'connectedAt': timestamp
            }
        )
        
        print(f"New connection established: {connection_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Connected successfully!')
        }
        
    except Exception as e:
        print(f"Error saving connection: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
