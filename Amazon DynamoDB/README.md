## Amazon DynamoDB in "Echoes of the Ancients"

Amazon DynamoDB is used in "Echoes of the Ancients" as the persistent data store for the game's state. <p>This allows players to save their progress and resume the game later without losing their place.


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
```
- DynamoDB Data Streming
```json
{
  "player_id": {
    "S": "test_player"
  },
  "current_location": {
    "S": "starting_chamber"
  },
  "inventory": {
    "L": [
      {
        "S": "torch"
      },
      {
        "S": "key"
      }
    ]
  },
  "progress": {
    "S": "You are in the starting chamber. You have taken the torch."
  },
  "quests": {
    "M": {
      "defeat_guard": {
        "M": {
          "description": {
            "S": "Defeated the guard in the north chamber."
          },
          "status": {
            "S": "completed"
          }
        }
      },
      "find_artifact": {
        "M": {
          "description": {
            "S": "Find the ancient artifact in the hidden room."
          },
          "status": {
            "S": "in-progress"
          }
        }
      }
    }
  }
}
```

**Workflow Summary:**
1.    When the game starts or a player loads a saved game, the load_game_state function is called.
2.    load_game_state retrieves the game state from DynamoDB using the player_id.
3.    During gameplay, when the player quits or explicitly saves the game, the save_game_state function is called.
4.    save_game_state saves the current game state to DynamoDB.

**Benefits of Using DynamoDB:**
*    **Persistence:** Game progress is saved and can be resumed later.
*    **Scalability:** Can handle a large number of players.
*    **Performance:** Fast read and write operations.
*    **Serverless:** No servers to manage.

### Recource
> Follow the Official Create a DynamoDB table [`Go Here`](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-1.html)