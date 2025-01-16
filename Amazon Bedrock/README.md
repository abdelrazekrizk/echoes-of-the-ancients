 # Amazon Bedrock in "Echoes of the Ancients"

Amazon Bedrock is a key component of "Echoes of the Ancients," providing access to powerful foundation models (FMs) that enable dynamic story generation and enhance the game's narrative. Unlike some other AWS services, you don't "create" a Bedrock service instance. Instead, you gain access to the service and its available models through your AWS account.

Here's a summary of how Bedrock is used, including the access and usage process:

**Key Functions:**

*   **Dynamic Story and Description Generation:** Bedrock is used to generate:
    *   Descriptions of locations when the player uses the `look` command.
    *   Descriptions of items when the player examines them.
    *   Potentially NPC dialogue or even dynamically generated story events in the future.
*   **Access to Foundation Models (FMs):** Bedrock provides access to a variety of FMs from different providers, such as AI21 Labs, Anthropic, Cohere, and Stability AI. In "Echoes of the Ancients," we are primarily using Anthropic's Claude model.
*   **Text Generation:** The FMs are used to generate text based on prompts provided by the Lambda function.

**Accessing and Using Amazon Bedrock:**

1.  **AWS Account and Region:** Ensure you have an AWS account and are working in a region where Bedrock is available. Not all regions support Bedrock.
2.  **Model Access:** In the Bedrock console, you can request access to specific models. This is typically a one-time process. Once access is granted, you can use the models in your applications.
3.  **Boto3 Integration:** The Lambda function uses the Boto3 library to interact with Bedrock:

```python
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

def generate_story_segment(prompt):
    body = {
        "prompt": prompt,
        "max_tokens_to_sample": 500 #Adjust as needed
    }
    try:
        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",  # Or your chosen model - make sure to request access to this model in the Bedrock console.
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get("body").read().decode())
        story_text = response_body["completion"]
        return story_text
    except Exception as e:
        print(f"Error calling Bedrock: {e}")
        return "An error occurred during story generation."
```
Summary:

The Lambda function determines that it needs to generate text (e.g., when the player uses the look command).
The Lambda function constructs a prompt based on the game context (e.g., the player's current location).
The Lambda function calls the generate_story_segment function, passing the prompt.
generate_story_segment uses Boto3 to call the Bedrock API.
Bedrock generates text based on the prompt and returns it to the Lambda function.
The Lambda function sends the generated text back to the game client (via Lex).