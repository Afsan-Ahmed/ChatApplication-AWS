"""
ChatDisconnect Lambda Function
Handles WebSocket disconnections

Author: Afsan Ahmed P.M.
"""

import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatConnections')

def lambda_handler(event, context):
    """
    Triggered when a user disconnects from the WebSocket API.
    Removes the connection ID from DynamoDB to clean up stale connections.
    
    Args:
        event: API Gateway WebSocket $disconnect event
        context: Lambda context object
    
    Returns:
        Success response with 200 status code
    """
    
    # Extract connection ID from the event
    connection_id = event['requestContext']['connectionId']
    
    try:
        # Remove connection from DynamoDB
        table.delete_item(
            Key={
                'connectionId': connection_id
            }
        )
        
        print(f"Connection disconnected: {connection_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Disconnected successfully!')
        }
        
    except Exception as e:
        print(f"Error removing connection: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
