# Add  or update Items in DynamoDB Table
import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()


# Get the profile name from environment or use a default profile
profile_name = os.getenv("AWS_PROFILE") # provide your profile name or set it in .env

# Create a session using the profile name
session = boto3.Session(profile_name=profile_name)


# Create clients using the session object
dynamodb = session.resource('dynamodb', region_name=os.getenv("region"))
# Initialize the DynamoDB resource object
table = dynamodb.Table('player_data')

# Example player data to save to the table
player_data = {
    'player_id': 'test_player',
    'progress': 'You are in the starting chamber. You have taken the torch.',
    'inventory': ['torch', 'key'],
    'current_location': 'starting_chamber',
    'quests': {
        'find_artifact': {
            'status': 'in-progress',
            'description': 'Find the ancient artifact in the hidden room.'
        },
        'defeat_guard': {
            'status': 'completed',
            'description': 'Defeated the guard in the north chamber.'
        }
    }
}

# Save the player data to DynamoDB table
table.put_item(Item=player_data)
