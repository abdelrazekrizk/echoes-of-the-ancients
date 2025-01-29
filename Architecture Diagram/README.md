## Architecture Diagram for "Echoes of the Ancients"

![Echoes of the Ancients Architecture](./Serverless-Game-Architectur(2).png)

**Explanation and Diagram Guide:**

1.  **Player Input (Text) --> Game Client (game.py):** The player interacts with the game's text interface (running in `game.py`).

2.  **Game Client (game.py) --> Amazon Cognito:** The `game.py` script initiates the authentication process with Amazon Cognito. This typically involves presenting a login form to the user (if they don't have an existing session) or checking for an existing authentication token.

3.  **Amazon Cognito --> Game Client (game.py):** Cognito authenticates the user (verifies their credentials) and, upon successful authentication, issues an access token (and potentially other tokens like an ID token and refresh token). This token is then used by the `game.py` script for subsequent requests.

4.  **Game Client (game.py) --> Amazon Lex (V1):** The `game.py` script now includes the access token (or a suitable authorization header) when sending requests to the Amazon Lex bot. This allows your backend (via API Gateway) to verify that the request is coming from an authenticated user.

5.  **Amazon Lex (V1) --> API Gateway:** Lex processes the input, determines the intent and slot values, and sends the request to API Gateway.  API Gateway is the entry point for all requests to your backend services.

6.  **API Gateway --> AWS Lambda (lex_handler.py):** API Gateway handles authentication (using the Cognito token), authorization, and routes the request to the appropriate AWS Lambda function (`lex_handler.py`).

7.  **AWS Lambda <--> Amazon DynamoDB:** The Lambda function interacts with DynamoDB to:
    *   Retrieve the current game state (player location, inventory, etc.).
    *   Save updated game state after the player performs an action. The double arrow `<-->` indicates two-way communication (read and write).

8.  **AWS Lambda <--> Amazon Bedrock:** When the Lambda function needs to generate a description or story segment (e.g., for the `LookIntent`), it calls the Amazon Bedrock API. Bedrock processes the request and returns the generated text to the Lambda function. The double arrow `<-->` indicates two-way communication (request and response).

9.  **AWS Lambda <--> Amazon S3:** When the Lambda function needs to retrieve lore or other assets, it interacts with Amazon S3. The double arrow `<-->` indicates two-way communication (request and response).

10. **AWS Lambda --> Amazon Polly --> Game Client (game.py):** When the Lambda function needs to speak some text, it sends the text to Amazon Polly. Polly generates the audio, which is sent back to the Lambda. The Lambda sends the audio data or a URL to the game client. The game client plays the audio.

11. **Amazon Lex <-- API Gateway <-- Amazon Lex:** The Lambda function constructs a response, which is sent back to API Gateway. API Gateway forwards the response to Lex, which then sends the response back to the `game.py` client to be displayed to the user.  API Gateway handles the response path as well.
