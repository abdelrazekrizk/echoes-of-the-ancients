## Architecture Diagram for "Echoes of the Ancients"

![Echoes of the Ancients Architecture](echoes-of-the-ancients-architecture.png)  *(Or your chosen filename)*


**Explanation and Diagram Guide:**

1.  **Player Input (Text) --> Game Client (game.py):** The player types a command into the game's text interface (running in `game.py`).

2.  **Game Client (game.py) --> Amazon Lex (V1):** The `game.py` script sends the player's text input to the Amazon Lex bot using the Lex Runtime API (`lex.post_text()`).

3.  **Amazon Lex (V1) --> AWS Lambda (lex_handler.py):** Lex analyzes the input, determines the intent and slot values, and invokes the configured AWS Lambda function (`lex_handler.py`). This is the *code hook*.

4.  **AWS Lambda <--> Amazon DynamoDB:** The Lambda function interacts with DynamoDB to:
    *   Retrieve the current game state (player location, inventory, etc.).
    *   Save updated game state after the player performs an action. The double arrow `<-->` indicates two-way communication (read and write).

5.  **AWS Lambda <--> Amazon Bedrock:** When the Lambda function needs to generate a description or story segment (e.g., for the `LookIntent`), it calls the Amazon Bedrock API. Bedrock processes the request and returns the generated text to the Lambda function. The double arrow `<-->` indicates two-way communication (request and response).

6.  **AWS Lambda <--> Amazon S3:** When the Lambda function needs to retrieve lore or other assets, it interacts with Amazon S3. The double arrow `<-->` indicates two-way communication (request and response).

7.  **AWS Lambda --> Amazon Polly --> Game Client (game.py):** When the Lambda function needs to speak some text, it sends the text to Amazon Polly. Polly generates the audio, which is sent back to the Lambda. The Lambda sends the audio data or a URL to the game client. The game client plays the audio.

8.  **Amazon Lex <-- AWS Lambda <-- Amazon Lex:** The Lambda function constructs a response in the format expected by Lex, which is then sent back to Lex. Lex then sends the response back to the `game.py` client to be displayed to the user.

