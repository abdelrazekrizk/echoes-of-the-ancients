# filename: lex_handler.py (This is the code for your Lambda function)
import json
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the profile name from environment or use a default
profile_name = os.getenv("AWS_PROFILE") # provide your profile name or set it in .env

# Create a session profile using the AWS SDK
session = boto3.Session(profile_name=profile_name)

# Create clients using the session for necessary AWS services
bedrock = session.client(service_name="bedrock-runtime", region_name=os.getenv("region"))
dynamodb = session.resource('dynamodb', region_name=os.getenv("region"))
table = dynamodb.Table('player_data')
lex = session.client('lex-runtime', region_name=os.getenv("region"))

# Define game locations and their descriptions
locations = {
    "starting_chamber": {
        "description": "You are in a dimly lit chamber.",
        "exits": {"north": "north_chamber"},
        "items": ["torch"]
    },
    "north_chamber": {
        "description": "You are in a cold, stone chamber.",
        "exits": {"south": "starting_chamber"},
        "items": ["key"]
    }
}

def generate_story_segment(prompt):
    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 500
    }
    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response['body'].read().decode())
        story_text = response_body["completion"]
        return story_text
    except Exception as e:
        print(f"Error calling Bedrock: {e}")
        return "An error has occurred."

def get_location_description(location):
    if location in locations:
        return locations[location]["description"]
    else:
        return "You are in an unknown location."

def save_player_progress(player_id, progress, inventory, current_location, quests):
    table.put_item(
        Item={
            'player_id': player_id,
            'progress': progress,
            'inventory': inventory,
            'current_location': current_location,
            'quests': quests
        }
    )  

def load_player_progress(player_id):
    response = table.get_item(Key={'player_id': player_id})
    return response.get('Item', {}).get('progress', "No saved progress found.")

def lambda_handler(event, context):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    session_attributes = event.get('sessionAttributes', {})
    player_id = session_attributes.get('player_id', 'test_player')

    if intent_name == 'GreetIntent':
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Greetings, traveler."
                }
            }
        }
    elif intent_name == 'AskAboutLocationIntent':
        location = slots.get('Location')
        if location:
            description = get_location_description(location)
            response = {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": description
                    }
                }
            }
        else:
            response = {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName": "AskAboutLocationIntent",
                    "slots": slots,
                    "slotToElicit": "Location",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Which location are you interested in?"
                    }
                }
            }
    elif intent_name == 'TakeIntent':
        item = slots.get('Item')
        if item:
            response = {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": f"You take the {item}."
                    }
                }
            }
        else:
            response = {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName": "TakeIntent",
                    "slots": slots,
                    "slotToElicit": "Item",
                    "message": {
                        "contentType": "PlainText",
                        "content": "What do you want to take?"
                    }
                }
            }
    elif intent_name == 'LookIntent':
        item = slots.get('LookedAtObject')
        if item:
            prompt = f"Describe the {item}."
            description = generate_story_segment(prompt)
            response = {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": description
                    }
                }
            }
        else:
            response = {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName": "LookIntent",
                    "slots": slots,
                    "slotToElicit": "LookedAtObject",
                    "message": {
                        "contentType": "PlainText",
                        "content": "What do you want to look at?"
                    }
                }
            }
    elif intent_name == 'SaveProgressIntent':
        progress = slots.get('Progress')  # Get the progress from the slot
        inventory = slots.get('Inventory', [])  # Assuming you might want to save inventory as well
        current_location = slots.get('CurrentLocation', 'starting_chamber')  # Default location
        quests = slots.get('Quests', {})  # Assuming you might want to save quests as well

        if progress:
            save_player_progress(player_id, progress, inventory, current_location, quests)
            response = {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Your progress has been saved."
                    }
                }
            }
        else:
            response = {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName": "SaveProgressIntent",
                    "slots": slots,
                    "slotToElicit": "Progress",
                    "message": {
                        "contentType": "PlainText",
                        "content": "What progress would you like to save?"
                    }
                }
            }
    elif intent_name == 'LoadProgressIntent':
        # Load player progress from DynamoDB
        progress = load_player_progress(player_id)
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": f"Your saved progress is: {progress}"
                }
            }
        }
    elif intent_name == 'InventoryIntent':
        # Provide inventory information
        inventory = "You have a torch and a key."  # Placeholder for actual inventory logic
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": f"Your inventory contains: {inventory}"
                }
            }
        }
    elif intent_name == 'MovementIntent':
        direction = slots.get('Direction')
        if direction:
            # Placeholder for movement logic
            response = {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Fulfilled",
                    "message": {
                        "contentType": "PlainText",
                        "content": f"You move {direction}."
                    }
                }
            }
        else:
            response = {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName": "MovementIntent",
                    "slots": slots,
                    "slotToElicit": "Direction",
                    "message": {
                        "contentType": "PlainText",
                        "content": "Which direction would you like to move?"
                    }
                }
            }
    else:
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "I don't understand that."
                }
            }
        }
    return response