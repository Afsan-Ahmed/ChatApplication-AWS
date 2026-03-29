"""
ChatSendMessage Lambda Function
Handles message broadcasting to all connected users

Author: Afsan Ahmed P.M.
"""

import json
import boto3
from datetime import datetime

# Initialize clients
dynamodb = boto3.resource('dynamodb')
connections_table = dynamodb.Table('ChatConnections')
messages_table = dynamodb.Table('ChatMessages')

def lambda_handler(event, context):
    """
    Triggered when a user sends a message through the WebSocket.
    
    Process:
    1. Parse the incoming message
    2. Save message to ChatMessages table
    3. Get all active connections from ChatConnections table
    4. Broadcast message to all connected users
    5. Clean up any stale connections
    
    Args:
        event: API Gateway WebSocket event with message data
        context: Lambda context object
    
    Returns:
        Success/error response
    """
    
    # Extract connection ID
    connection_id = event['requestContext']['connectionId']
    
    # Parse message from request body
    try:
        body = json.loads(event.get('body', '{}'))
        message = body.get('message', '')
        username = body.get('username', 'Anonymous')
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid message format')
        }
    
    # Validate message
    if not message or len(message.strip()) == 0:
        return {
            'statusCode': 400,
            'body': json.dumps('Message cannot be empty')
        }
    
    # Create timestamp and message ID
    timestamp = int(datetime.now().timestamp())
    message_id = f"{timestamp}-{connection_id}"
    
    try:
        # Save message to DynamoDB
        messages_table.put_item(
            Item={
                'messageId': message_id,
                'timestamp': timestamp,
                'username': username,
                'message': message,
                'connectionId': connection_id
            }
        )
        
        print(f"Message saved: {message_id}")
        
        # Get all active connections
        response = connections_table.scan()
        connections = response.get('Items', [])
        
        print(f"Broadcasting to {len(connections)} connections")
        
        # Initialize API Gateway Management API client
        # This allows us to send messages back to WebSocket clients
        domain_name = event['requestContext']['domainName']
        stage = event['requestContext']['stage']
        apigw_management = boto3.client(
            'apigatewaymanagementapi',
            endpoint_url=f"https://{domain_name}/{stage}"
        )
        
        # Prepare broadcast message
        broadcast_data = json.dumps({
            'username': username,
            'message': message,
            'timestamp': timestamp
        })
        
        # Broadcast to all connections
        failed_connections = []
        
        for connection in connections:
            try:
                # Send message to each connection
                apigw_management.post_to_connection(
                    ConnectionId=connection['connectionId'],
                    Data=broadcast_data.encode('utf-8')
                )
            except apigw_management.exceptions.GoneException:
                # Connection is stale (user disconnected but not cleaned up)
                print(f"Stale connection found: {connection['connectionId']}")
                failed_connections.append(connection['connectionId'])
            except Exception as e:
                print(f"Error sending to {connection['connectionId']}: {str(e)}")
                failed_connections.append(connection['connectionId'])
        
        # Clean up stale connections
        for failed_connection_id in failed_connections:
            try:
                connections_table.delete_item(
                    Key={'connectionId': failed_connection_id}
                )
                print(f"Cleaned up stale connection: {failed_connection_id}")
            except Exception as e:
                print(f"Error cleaning up connection: {str(e)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Message sent successfully',
                'broadcast_count': len(connections) - len(failed_connections)
            })
        }
        
    except Exception as e:
        print(f"Error in message handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
