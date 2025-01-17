# Amazon Lex

**Objective:** Create a chatbot named GameSage designed to enhance player engagement in our text-based adventure game.<p>This bot will serve as a virtual game guide, allowing players to navigate the game world,interact with objects, solve puzzles, engage in combat, and manage inventory seamlessly.<p>The bot will use intents such as movement, item collection, trading, quest management, and more to offer an immersive experience.<p>Players can ask for help, seek hints, or explore game lore interactively.<p>Slots like Location, Item, and Action ensure the bot processes user commands contextually.<p>`GameSage` will also handle dynamic conversations for trading and questsoffering a responsive, player-centric<p>

## Amazon Lex in "Echoes of the Ancients"

Amazon Lex plays a crucial role in "Echoes of the Ancients" by providing natural language understanding (NLU) capabilities. It allows players to interact with the game using natural language, making the experience more intuitive and immersive than simply typing rigid commands.

Here's a summary of how Lex  is used, including its creation and Lambda integration:

**Key Functions:**

*   **Natural Language Understanding (NLU):** Lex analyzes player input (text) and attempts to understand the player's intent (what they want to do).
*   **Intent Recognition:** Lex identifies the specific action the player wants to perform. These actions are defined as *intents* in the Lex bot configuration.
*   **Slot Extraction:** Along with identifying the intent, Lex extracts specific pieces of information from the player's input. These pieces of information are called *slots*.
*   **Dialog Management (Limited in this context):** We are using a simplified approach. The primary use of Lex is to recognize intents and extract slots, which are then passed to the
Lambda function.
*   **Integration with Lambda:** Lex acts as a trigger for an AWS Lambda function (our code hook). Once Lex has processed the player input, it invokes the Lambda function and passes the identified intent and slot values as an event.

**Key Concepts in Our Lex Bot Configuration:**

*   **Intents:** Represent actions the player can perform. Examples:
    *   `SageBot_Greetings_Intent` (e.g., "hello", "hi")
    *   `SageBot_Location_Intent` (e.g., "where am I", "tell me about this place")
    *   `SageBot_Item_Intent` (e.g., "take the key", "grab torch")
    *   `SageBot_Look_In_Object_Intent` (e.g., "look around", "examine the table")
    *   `SageBot_Direction_Intent` (e.g., "go north", "head east", "south")
    *   `SageBot_Inventory_Intent` (e.g., "inventory", "what do I have")

*   **Slots:** Represent pieces of information associated with an intent. Examples:
    *   `Location` (used with `SageBot_Location_Intent`, values: "starting_chamber", "north_chamber", etc.)
    *   `Item` (used with `SageBot_Item_Intent`, values: "key", "torch", "coin", etc.)
    *   `Look_In` (used with `SageBot_Look_In_Object_Intent`, values: "key", "torch", "coin", etc. - a duplicate slot type is used to avoid conflicts)
    *   `Direction` (used with `SageBot_Direction_Slot`, values: "north", "south", "east", "west")

*   **Slot Types:** Define the possible values for a slot. We use custom slot types to define game-specific entities like locations and items.

**Creating the Lex Bot and Integrating with Lambda:**

1.  **Bot SageBot_Direction_Intention:** The Lex bot is SageBot_Direction_Intented in the AWS Lex  console.
2.  **Intent and Slot Definition:** Intents and custom slot types are defined within the bot configuration, including sample utterances for training the NLU model.
3.  **Slot Association with Intents:** Slots are associated with the appropriate intents. For example, the `Location` slot is associated with the `SageBot_Location_Intent` and `SageBot_Direction_Intent` intents.
4.  **Lambda Function SageBot_Direction_Intention:** An AWS Lambda function (`lex_handler.py`) is SageBot_Direction_Intented to act as the code hook for the Lex bot. This function contains the game's backend logic.
5.  **Lambda Integration in Lex:** In the Lex bot configuration, the Lambda function is specified as the fulfillment method for each intent. This establishes the connection between Lex and Lambda.
6.  **Bot Building:** After configuring the intents, slots, and Lambda integration, the Lex bot is built. This compiles the bot's definition and makes it ready to process user input.

**Workflow Summary:**

1.  Player enters text.
2.  Text is sent to Lex.
3.  Lex recognizes the intent and extracts slot values.
4.  Lex invokes the Lambda function, passing the intent and slots as an event.
5.  The Lambda function processes the request and sends a response back to Lex.
6.  Lex sends the response to the game client.


# Lex Chat Bot Structure:

```markdown
C:.
└───GameSage
    └───BotLocales
        └───en_US
            ├───Intents
            │   ├───FallbackIntent
            │   ├───SageBot_Action_Command_Intent
            │   │   └───Slots
            │   │       └───Action_Command
            │   ├───SageBot_Character_Dialogue_Intent
            │   │   └───Slots
            │   │       └───Character_Dialogue
            │   ├───SageBot_Direction_Intent
            │   │   └───Slots
            │   │       └───Directions
            │   ├───SageBot_Fallback_Intent
                ├───SageBot_Greetings_Intent
            │   ├───SageBot_Game_Settings_Intent
            │   ├───SageBot_Help_Intent
            │   │   └───Slots
            │   │       └───Help
            │   ├───SageBot_Hint_Topic_Intent
            │   │   └───Slots
            │   │       └───Hint_Topic
            │   ├───SageBot_Inventory_Intent
            │   │   └───Slots
            │   │       └───Inventory
            │   ├───SageBot_Item_Intent
            │   │   └───Slots
            │   │       └───Item
            │   ├───SageBot_Load_Progress_Intent
            │   ├───SageBot_Location_Intent
            │   │   └───Slots
            │   │       └───location
            │   ├───SageBot_Look_In_Object_Intent
            │   │   └───Slots
            │   │       └───Look_In
            │   ├───SageBot_Quests_Intent
            │   ├───SageBot_Save_Progress_Intent
            │   └───SageBot_User_Progress_Intent
            └───SlotTypes
                ├───SageBot_Action_command_Slot
                ├───SageBot_Character_Dialogue_Slot
                ├───SageBot_Direction_Slot
                ├───SageBot_Help_Slot
                ├───SageBot_Hint_Topic_Slot
                ├───SageBot_Inventory_Slot
                ├───SageBot_Item_Slot
                ├───SageBot_Location_Slot
                └───SageBot_Look_In_Object_Slot
```

# Intents and Slots:

1. **SageBot_Action_Command_Intent**
   - **Slot Name:** Action_Command
   - **Slot Type:** SageBot_Action_command_Slot
   - **Elicitation Prompt:** "What action would you like to perform?"
   - **Sample Utterances:** "Move forward", "Attack the enemy", "Use the key", "Defend against the attack", "Move to the north", "Use the torch"

2. **SageBot_Fallback_Intent**
   - **Slots:** None
   - **Sample Utterances:** "I do not understand", "Can you do that", "What do you mean", "That is not what I meant", "Help me with that", "I'm not sure what to say"

3. **SageBot_Load_Progress_Intent**
   - **Slots:** None
   - **Sample Utterances:** "Load my last save", "Resume my game", "Open save slot", "Retrieve my last save", "Continue from my last checkpoint", "Start where I left off"

4. **SageBot_Look_In_Object_Intent**
   - **Slot Name:** Look_In
   - **Slot Type:** SageBot_Look_In_Object_Slot
   - **Elicitation Prompt:** "What do you want to examine?"
   - **Sample Utterances:** "Look at the statue", "Examine the table", "Inspect the book", "Check the painting", "Observe the vase", "Gaze at the tapestry"

5. **SageBot_Quests_Intent**
   - **Slots:** None
   - **Sample Utterances:** "Show me my active quests", "Update my quest status", "List my completed quests", "Check my quest progress", "Tell me about my current quests", "What is my next Quest", "What Quests do I have"

6. **SageBot_Save_Progress_Intent**
   - **Slots:** None
   - **Sample Utterances:** "Save my progress", "SageBot_Direction_Intente a save point", "Can I save my game", "I want to save that I have reached the north chamber.", "Save that I have taken the key.", "I need to save my current location.", "Please save my game", "Record my current status"

7. **SageBot_Character_Dialogue_Intent**
   - **Slot Name:** Character_Dialogue
   - **Slot Type:** SageBot_Character_Dialogue_Slot
   - **Elicitation Prompt:** "Which one would you like to speak with?"
   - **Sample Utterances:** "Talk to the merchant", "Ask the guard about the key", "Speak to the wizard for advice", "Can I get help from the healer", "Converse with the merchant", "Inquire with the guard", "Chat with the wizard"

8. **SageBot_Direction_Intent**
   - **Slot Name:** Directions
   - **Slot Type:** SageBot_Direction_Slot
   - **Elicitation Prompt:** "Which direction would you like to move?"
   - **Sample Utterances:** "Move north", "Go south", "Travel east", "Head west", "Advance upward", "Descend downward", "Step backward", "Turn left", "Turn right"

9. **SageBot_Game_Settings_Intent**
   - **Slots:** None
   - **Sample Utterances:** "Change difficulty to hard", "Adjust sound", "Adjust sound to medium", "Set text speed to fast", "Lower the volume", "Increase the difficulty level", "Set graphics to high"

10. **SageBot_Location_Intent**
    - **Slot Name:** location
    - **Slot Type:** SageBot_Location_Slot
    - **Elicitation Prompt:** "Which location would you like to know more about?"
    - **Sample Utterances:** "Tell me about the chamber", "What is this place", "Describe the room", "Where is the chamber", "Where is the room", "Where is the hallway", "Where is the starting chamber", "Where is the north chamber", "Where is the east chamber", "Where is the hidden room", "Tell me about the dark forest", "Describe the treasure cave", "What are the ancient ruins like"

11. **SageBot_User_Progress_Intent**
    - **Slots:** None
    - **Sample Utterances:** "What is my progress", "Recap the story", "What have I done so far", "Give me an update on my story", "Tell me about my journey", "Show me my achievements"

12. **SageBot_Help_Intent**
    - **Slot Name:** Help
    - **Slot Type:** SageBot_Help_Slot
    - **Elicitation Prompt:** "What would you like help with? For example, exploring, commands, or map guidance?"
    - **Sample Utterances:** "I need help", "What can I do", "List commands", "Help me with exploring", "Show me the map", "How do I use commands", "I need help with exploring", "Give me some combat tips", "How do I manage my inventory"

13. **SageBot_Item_Intent**
    - **Slot Name:** Item
    - **Slot Type:** SageBot_Item_Slot
    - **Elicitation Prompt:** "Which item do you want to take?"
    - **Sample Utterances:** "Take the torch", "Grab the key", "Pick up the coin", "I want the map", "Can I take the torch", "Get the key for me"

14. **SageBot_Hint_Topic_Intent**
    - **Slot Name:** Hint_Topic
    - **Slot Type:** SageBot_Hint_Topic_Slot
    - **Elicitation Prompt:** "Which location would you like to know more about? For example, hidden room or locked door?"
    - **Sample Utterances:** "I need a hint", "What should I do next", "Any clues for the hidden room", "Any clues for the locked door", "Can you give me a hint", "Help me with the puzzle", "What can you tell me about the north chamber"

15. **SageBot_Inventory_Intent**
    - **Slot Name:** Inventory
    - **Slot Type:** SageBot_Inventory_Slot
    - **Elicitation Prompt:** "Which item do you want to view or use?"
    - **Sample Utterances:** "What am I carrying", "List my inventory", "Check my items", "Show me my inventory", "What items do I have", "Display my carried items"
