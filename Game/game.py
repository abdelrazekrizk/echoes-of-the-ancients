import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

# Get the profile name from environment or use a default
profile_name = os.getenv("AWS_PROFILE")  # Provide your profile name or set it in .env

# Create a session using the profile
session = boto3.Session(profile_name=profile_name)

# Create clients using the session
bedrock = session.client(service_name="bedrock-runtime", region_name=os.getenv("region"))
dynamodb = session.resource('dynamodb', region_name=os.getenv("region"))
table = dynamodb.Table('player_data')
lex = session.client('lex-runtime', region_name=os.getenv("region"))

# Game world data (locations and items)
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
            modelId="anthropic.claude-v2",  # Or your chosen model
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response["body"].read().decode())
        story_text = response_body["completion"]
        return story_text
    except Exception as e:
        print(f"Error calling Bedrock: {e}")
        return "An error has occurred."

def save_game_state(player_id, location, inventory):
    try:
        table.put_item(
            Item={
                'player_id': player_id,
                'location': location,
                'inventory': inventory
            }
        )
        print("Game state saved.")
    except Exception as e:
        print(f"Error saving game state: {e}")

def load_game_state(player_id):
    try:
        response = table.get_item(Key={'player_id': player_id})
        if 'Item' in response:
            return response['Item']
        else:
            return None
    except Exception as e:
        print(f"Error loading game state: {e}")
        return None

def get_location_description(location):
    if location in locations:
        return locations[location]["description"]
    else:
        return "You are in an unknown location."

def talk_to_lex(user_input, session_attributes):
    try:
        response = lex.post_text(
            botName='GameInteractions',  # Replace with your bot name
            botAlias='Prod',              # Replace with your bot alias
            userId='testuser',            # Replace with a more robust user ID later
            inputText=user_input,
            sessionAttributes=session_attributes
        )
        return response
    except Exception as e:
        print(f"Error calling Lex: {e}")
        return {"message": "An error occurred communicating with the game."}

def main():
    player_id = "test_player"  # Replace with a more robust user ID later
    game_state = load_game_state(player_id)
    session_attributes = {'player_id': player_id}  # Initialize session attributes

    if game_state:
        print("Loading saved game...")
        location = game_state['location']
        inventory = game_state['inventory']
    else:
        print("Welcome to Echoes of the Ancients!")
        location = "starting_chamber"
        inventory = []
        print(get_location_description(location))

    while True:
        action = input("> ").lower()
        if action == "quit":
            save_game_state(player_id, location, inventory)
            break
        elif action.startswith("talk"):  # Handle talking to NPCs
            npc_input = action[5:].strip()  # Extract the text after "talk"
            lex_response = talk_to_lex(npc_input, session_attributes)
            print(lex_response['message'])
            session_attributes = lex_response.get('sessionAttributes', session_attributes)  # Update session attributes
        elif action == "look":
            print(get_location_description(location))
        elif action == "inventory":
            if inventory:
                print("You are carrying:")
                for item in inventory:
                    print(f"- {item}")
            else:
                print("You are carrying nothing.")
        elif action.startswith("go"):
            direction = action[3:].strip()
            if direction in locations[location]["exits"]:
                location = locations[location]["exits"][direction]
                print(get_location_description(location))
            else:
                print("You can't go that way.")
        elif action.startswith("take"):
            item_name = action[5:].strip()
            if item_name in locations[location]["items"]:
                inventory.append(item_name)
                locations[location]["items"].remove(item_name)
                print(f"You take the {item_name}.")
            else:
                print(f"There is no {item_name} here.")
        else:
            lex_response = talk_to_lex(action, session_attributes)  # Send other input to Lex
            print(lex_response['message'])
            session_attributes = lex_response.get('sessionAttributes', session_attributes)  # Update session attributes

if __name__ == "__main__":
    main()  