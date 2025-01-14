## Amazon DynamoDB in "Echoes of the Ancients"

Amazon DynamoDB is used in "Echoes of the Ancients" as the persistent data store for the game's state. This allows players to save their progress and resume the game later without losing their place.

Here's a summary of how DynamoDB is used:

**Key Functions:**

*   **Persistent Data Storage:** DynamoDB stores key game data that needs to be preserved between game sessions. This includes:
    *   Player's current location.
    *   Player's inventory (the items they are carrying).
    *   Potentially other game state information in the future (e.g., game progress, puzzle solutions, character stats).
*   **NoSQL Database:** DynamoDB is a NoSQL database, which is well-suited for storing simple key-value pairs or document-like data. This makes it a good fit for storing game state, which can be represented as a JSON object.
*   **Scalability and Performance:** DynamoDB is highly scalable and provides fast read and write performance, making it suitable for handling a large number of players if the game were to grow.
*   **Integration with Lambda:** The Lambda function interacts with DynamoDB to save and load game state.

**Key Concepts and Implementation Details:**

*   **Table:** A DynamoDB table named `player_data` is created to store the game state.
*   **Primary Key:** The table uses `player_id` (String) as the primary key. This uniquely identifies each player's saved game.
*   **Data Structure:** The game state is stored as a JSON object with the following structure:

```json
{
  "player_id": "test_player", // Unique identifier for the player
  "location": "starting_chamber", // Current location of the player
  "inventory": ["torch"] // Array of items in the player's inventory
}