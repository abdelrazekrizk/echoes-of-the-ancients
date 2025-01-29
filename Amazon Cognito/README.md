## Amazon Cognito in "Echoes of the Ancients"

Amazon Cognito provides user authentication and authorization for "Echoes of the Ancients," ensuring secure access to the game and its underlying AWS resources. It manages user accounts, handles authentication, and issues access tokens that the game client (`game.py`) uses to interact with other AWS services.

**Key Functions:**

*   **User Authentication:** Manages user registration, sign-in, and password management.
*   **Authorization:** Controls access to the game and its resources using access tokens.
*   **Identity Management:** Provides a secure way to store and manage user identities.
*   **Integration with Game Client:** The `game.py` script integrates with the Cognito SDK to handle authentication and token management.

**Setting up Amazon Cognito:**

1.  **Create a User Pool:**
    *   In the AWS Management Console, navigate to the Amazon Cognito service.
    *   Click "Create user pool."
    *   Choose "Cognito User Pool" and click "Next."
    *   Configure the user pool settings:
        *   **Pool name:** Give your user pool a descriptive name (e.g., `echoes-of-the-ancients-user-pool`).
        *   **Authentication providers:** Choose the authentication methods you want to support (e.g., username/password, social logins).
        *   **Sign-up experience:** Customize the sign-up process (e.g., required attributes).
        *   **Message delivery:** Configure how users receive verification codes (email, SMS).
        *   **App client settings:** Configure settings for your game client (e.g., allowed OAuth flows).
        *   **Advanced settings:** Configure advanced settings (e.g., password policies, multi-factor authentication).
    *   Click "Create user pool."

2.  **Create an App Client:**
    *   Within your user pool, navigate to "App integration" -> "App clients."
    *   Click "Create app client."
    *   **App client name:** Give your app client a descriptive name (e.g., `echoes-of-the-ancients-game-client`).
    *   **Client secret:** Choose whether to generate a client secret.  For a pure text-based game, you might not need a client secret.
    *   **Allowed OAuth flows:** Select the appropriate OAuth flows (e.g., Authorization code grant).
    *   **Allowed callback URLs:** Specify the URLs where Cognito should redirect users after authentication.  For a text-based game running locally, this might not be strictly necessary, but you should still set a placeholder.
    *   Click "Create app client."

3.  **Integrate Cognito with `game.py` (using AWS_PROFILE):**
    *   Install the AWS SDK for Python (Boto3): `pip install boto3`
    *   Update your `game.py` script to use the Cognito SDK and the `AWS_PROFILE` environment variable:

```python
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Get the profile name from environment or use a default
profile_name = os.getenv("AWS_PROFILE")

# Create a session using the profile
session = boto3.Session(profile_name=profile_name)

cognito_client = session.client('cognito-idp', region_name=os.getenv("AWS_DEFAULT_REGION")) # Use the session
USER_POOL_ID = "your-user-pool-id"  # Replace with your User Pool ID
APP_CLIENT_ID = "your-app-client-id" # Replace with your App Client ID

def authenticate_user(username, password):
    try:
        response = cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId=APP_CLIENT_ID,
            UserPoolId=USER_POOL_ID
        )
        access_token = response['AuthenticationResult']['AccessToken']
        return access_token
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

# Example usage:
username = input("Enter username: ")
password = input("Enter password: ")

access_token = authenticate_user(username, password)

if access_token:
    print("Authentication successful!")
    # Use the access token to interact with other AWS services
    # ...
else:
    print("Authentication failed.")