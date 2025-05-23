# Echoes of the Ancients: A Text-Based Adventure Game on AWS

## Project Overview

"Echoes of the Ancients" is a text-based adventure game built entirely on AWS serverless technologies.<p> Players explore ancient ruins, interacting with the environment and non-player characters (NPCs) through text commands. <p>The game leverages Amazon Bedrock for dynamic story generation, Amazon Lex for natural language understanding, Amazon DynamoDB for persistent game state, and Amazon S3 for storing game assets. It also incorporates Amazon Polly for text-to-speech functionality. <p>This project demonstrates a practical application of serverless architecture for game development, showcasing scalability, cost-effectiveness, and the integration of AI services.

---

## Purpose

This project was created for the `AWS Game Builder Challenge` to demonstrate the capabilities of AWS services in building interactive games. It specifically focuses on:


*   **Serverless Architecture:** Utilizing `Lambd`a, API Gateway (if we add a web interface later), and `DynamoDB` to create a scalable and cost-effective game backend.
*   **AI Integration:** Leveraging `Amazon Bedrock` for dynamic and engaging narrative experiences, `Amazon Lex` for natural language understanding, and `Amazon Polly` for immersive audio.
*   **Text-Based Adventure Genre:** Exploring the classic text adventure genre with modern AI enhancements.
---

## How to Run the Game

1.  **Prerequisites:**
    *   Python 3.12 or later installed.
    *   AWS CLI configured with appropriate credentials (including access to Bedrock, DynamoDB, Lex, Polly, and S3).
    *   A virtual environment (recommended).
    *   A DynamoDB table named `player_data` with a primary key `player_id` (String).
    *   A Lex  bot named `SageBot` (or your chosen name) configured with the correct intents and slots, and connected to the Lambda function.
    *   A Lambda function configured with access to Bedrock and DynamoDB.
    *   An S3 bucket for storing game assets .
2.  **Setup:**
    *   Clone the repository (once it's public).
    *   Navigate to the project directory: `cd echoes-of-the-ancients`
    *   Create and activate a virtual environment:
        *   `python3 -m venv .venv`
        *   `source .venv/bin/activate` (Linux/macOS)
        *   `.venv/Scripts/activate` (Windows)
    *   Install the required packages: `pip install -r requirements.txt` (Make sure `playsound` is in your `requirements.txt`)
    *   Create a `.env` file in the project root and add your AWS credentials:
*    **AWS IAM Identity Center:**
       ```markdown
        AWS_PROFILE=   # Your SSO profile name
        region=        # Your AWS region e.g., us-east-1
       ```
*    **AWS Identity and Access Management:**
        ```markdown
        AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
        AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
        AWS_DEFAULT_REGION=YOUR_AWS_REGION
        ```

3.  **Run the Game:**
    *   Execute the game script: `python3 game.py`
---

## Game Features and Gameplay

The game is a text-based adventure where you explore locations, interact with objects, and potentially communicate with NPCs.

*   **Movement:** Use commands like `go north`, `go south`, `north`, `south` etc. to move between locations.
*   **Looking Around:** Use commands like `look`, `describe`, or `examine` to get a description of your current location. These descriptions are also spoken using Amazon Polly.
*   **Taking Items:** Use commands like `take key` or `grab torch` to add items to your inventory.
*   **Inventory:** Use commands like `inventory`, `items`, or `what do I have` to see what you're carrying.
*   **Talking to NPCs:** Use commands like `talk to guard` (if there's a guard in the current location) to initiate a conversation. NPC responses are also spoken using Amazon Polly.
*   **Reading Lore:** Use commands like `read ancient_scroll` to access background information stored in S3.
*   **Saving and Quitting:** Use `save game` to save your progress and `quit` or `exit` to exit the game.
---

## Architecture Diagram for "Echoes of the Ancients"

![Echoes of the Ancients Architecture](./Architecture%20Diagram/Serverless-Game-Architectur.png)

**Workflow:**

1.  Player enters a text command.
2.  The command is sent to Amazon Lex.
3.  Lex processes the input and invokes the Lambda function.
4.  The Lambda function:
    *   Retrieves game state from DynamoDB.
    *   Generates descriptions using Bedrock (if needed).
    *   Retrieves lore from S3 (if needed).
    *   Updates game state.
    *   Sends a response back to Lex.
5.  Lex relays the response to the player.
6.  The game client uses Polly to speak the text responses.
---

## Technical Architecture

"Echoes of the Ancients" utilizes a combination of serverless and managed AWS services to deliver a dynamic and engaging text-based adventure.
The architecture is designed for scalability, security, and cost-effectiveness.

**Core Components:**

*   **Amazon Lex :** Handles natural language understanding (NLU). Lex interprets player input, identifies intents (actions), and extracts slots (information) to understand player commands.

*   **AWS Lambda:** Serves as the game's backend logic. Lambda functions are triggered by events from Lex and perform the following tasks:
    *   Managing game state (player location, inventory, etc.).
    *   Interacting with Amazon DynamoDB for persistent data storage.
    *   Generating dynamic story content and descriptions using Amazon Bedrock.
    *   Retrieving lore and other assets from Amazon S3.
    *   Providing text-to-speech output via Amazon Polly.

*   **Amazon Bedrock:** Provides access to powerful foundation models (FMs) for dynamic story and description generation.  This allows for a more immersive and unpredictable narrative experience.

*   **Amazon DynamoDB:** Stores persistent game data, ensuring that player progress is saved between sessions.

*   **Amazon S3:** Stores static game assets, such as lore text files, images, or other multimedia.

*   **Amazon Polly:** Provides text-to-speech functionality, enhancing immersion by "speaking" descriptions and NPC dialogue.

*   **Amazon Cognito:** Manages user authentication and authorization.  Players authenticate through Cognito to securely access the game.  This ensures that only authorized users can interact with the game and protects the underlying AWS resources.

*   **Amazon API Gateway:** Acts as the entry point for all requests to the game's backend (Lambda).  API Gateway handles authentication (using Cognito), authorization, request routing, and other essential tasks. This provides a secure and scalable interface for the game.

*   **Amazon EC2:**  (Current Deployment) Currently, the core game application (`game.py`) is deployed and runs on an Amazon EC2 instance.  While the architecture is primarily serverless, EC2 is used for hosting the main game logic.  Future enhancements will explore containerization with ECS.

**Data Flow and Interactions:**

1.  **Player Interaction:** Players interact with the game through a text-based interface.

2.  **Authentication:** The game client (`game.py`) interacts with Amazon Cognito to authenticate the player. Upon successful authentication, Cognito returns an access token.

3.  **Command Processing:** The game client sends player commands (text) along with the access token to Amazon Lex.

4.  **Intent Recognition and Slot Extraction:** Lex processes the command, identifies the player's intent, and extracts relevant information (slots).

5.  **API Gateway Routing and Authorization:** Lex sends the processed command to Amazon API Gateway. API Gateway verifies the access token provided by the client and, if valid, routes the request to the appropriate Lambda function.

6.  **Game Logic Execution:** The Lambda function executes the game logic based on the player's intent and extracted slots.  This may involve:
    *   Retrieving and updating game state in DynamoDB.
    *   Generating dynamic content using Bedrock.
    *   Accessing assets from S3.
    *   Generating text-to-speech output via Polly.

7.  **Response:** The Lambda function returns a response to API Gateway, which then forwards it to Lex, and finally back to the game client.

8.  **Audio Output:** If the response includes text to be spoken, the Lambda function uses Polly to generate speech, which is then played by the game client.

---
## Use of Amazon Q

Amazon Q was used throughout the development process to enhance various aspects of the project:

*   **Code Generation:** Amazon Q assisted in generating boilerplate code for interacting with AWS services (Boto3 calls for Bedrock, DynamoDB, Lex, Polly, and S3).
*   **Code Explanation and Review:** Q was used to review code snippets, providing explanations and suggesting improvements.
*   **Code Commenting:** Q helped generate more detailed and consistent comments.
*   **Documentation Assistance:** Q assisted in writing parts of this README file.
*   **VS Code Integration:** Using the Amazon Q extension for VS Code provided real-time code suggestions and error detection.
---

## Future Enhancements

*   More complex game mechanics.
*   More advanced use of Bedrock for dynamic story generation and NPC interactions.
*   A web-based or other richer user interface.
*   Improved player ID management.
*   **Voice Interaction (Amazon Transcribe):** Implement speech-to-text functionality to allow players to use voice commands. This would involve capturing audio from the player's microphone, sending it to Amazon Transcribe for transcription, and then processing the transcribed text as game input.
*   More advanced audio features (background music, sound effects).
*   **Containerization (ECS):** Migrating the game application to Amazon Elastic Container Service (ECS) is planned for future enhancements.  This will improve deployment, scalability, and resource utilization.

---
## Recource
- AWS Identity and Access Management Documentation [`Go Here`](https://docs.aws.amazon.com/iam/)
iam identy center
-  Amazon Simple Storage Service Documentation [`Go Here`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
-  Amazon DynamoDB Documentation [`Go Here`](https://docs.aws.amazon.com/dynamodb/)
-  AWS Lambda Documentation [`Go Here`](https://docs.aws.amazon.com/lambda/)
-  Amazon API Gateway Documentation [`Go Here`](https://docs.aws.amazon.com/apigateway/)
-  Amazon Cognito Documentation [`Go Here`](https://docs.aws.amazon.com/cognito/)
-  Amazon Polly Documentation [`Go Here`](https://docs.aws.amazon.com/polly/)
-  Amazon Lex Documentation [`Go Here`](https://docs.aws.amazon.com/lex/)
-  Amazon EC2 Documentation [`Go Here`](https://docs.aws.amazon.com/ec2/)
-  Amazon Bedrock Documentation [`Go Here`](https://docs.aws.amazon.com/bedrock/)
