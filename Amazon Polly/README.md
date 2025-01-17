## Amazon Polly in "Echoes of the Ancients"

Amazon Polly enhances the user experience in "Echoes of the Ancients" by providing text-to-speech (TTS) functionality. <p>This allows game descriptions, NPC dialogue, and other text to be spoken aloud, adding another layer of immersion to the text-based adventure.<p>
Like Bedrock, Polly is a service you access; you don't create a specific Polly "instance."
**Key Functions:**

*   **Text-to-Speech (TTS):** Converts text into natural-sounding speech.
*   **Variety of Voices:** Polly offers a wide range of voices (different genders, accents, and languages) to choose from. In "Echoes of the Ancients," we use the "Joanna" voice as an example, but this can be easily changed.
*   **Integration with Lambda:** The Lambda function uses the Boto3 library to interact with Polly.

**Accessing and Using Amazon Polly:**

1.  **AWS Account and Region:** Ensure you have an AWS account and are working in a region where Polly is available.
2.    **Install via pip:**

    ```python
    pip install playsound3
    ```

3.  **Boto3 Integration:** The Lambda function uses the Boto3 library to
interact with Polly. Here's the relevant code:


```python
import os
import boto3
import json
from playsound3 import playsound
from dotenv import load_dotenv

load_dotenv()

# Get the profile name from environment or use a default
profile_name = os.getenv("AWS_PROFILE")  # Provide your profile name or set it in .env

# Create a session using the profile
session = boto3.Session(profile_name=profile_name)

# Create clients using the session
polly = session.client(service_name="bedrock-runtime", region_name=os.getenv("region"))

def speak_text(text):
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            response = polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId='Joanna'  # Or your preferred voice
            )
            with open(temp_file.name, 'wb') as f:
                f.write(response['AudioStream'].read())
            playsound.playsound(temp_file.name)
            os.remove(temp_file.name)
    except Exception as e:
        print(f"Error calling Polly: {e}")
        print(text)  # Fallback to printing the text
```
**Workflow Summary:**
1.    The Lambda function determines that it needs to speak some text (e.g., after generating a location description or receiving a Lex response).
2.    The Lambda function calls the speak_text function, passing the text.
3. speak_text uses Boto3 to call the Polly API.
4.    Polly generates the audio and returns it to the Lambda function.
5.    The Lambda function plays the audio.

**Benefits of Using Polly:**
*    Enhanced Immersion: Adds another dimension to the game experience by providing audio output.
*    Variety of Voices: Allows for customization and creating distinct character voices.
*    Easy Integration with Lambda: Seamless integration with other AWS services.
