
# Mancala Game

## Rules of the Game

### Game Setup:

- Two rows with six pits each.
- Player 1 (top row, CPU Player) and Player 2 (bottom row, Human Player).
- Each player has a home (leftmost and rightmost pits) which keeps track of their points.
- The game starts out with 4 stones per pit.

### Objective:
- Capture more stones than your opponent.
- Game ends when all pits on one side are empty.

### Gameplay:

#### Starting the Game:

- Players take turns; 
- Player 2 (so the human player) starts.

#### Turn Mechanics:

- Select a pit, pick up its stones, and distribute counterclockwise. This is all simulated in one click.
- If the last stone lands in the player's home, they get another turn.

#### Capturing Stones:

- If the last stone lands in an empty pit on the player's side, and the opposite pit on the opponent's side has stones, capture all those stones.

#### End Game:

- Game ends when one player's pits are empty.
- Remaining stones on the opponent's side are captured.

#### Determining the Winner:

- Count seeds in the store; player with the most seeds wins.

## Implementation:

### Initializing the Game:

- Initialize pits with stones using nested loops (2x6). Complexity: O(1).

### Handling Player Inputs:

- Methods handle user inputs and perform validation.

### Moving Stones:

- Stone movement based on the number of stones and their path. Worst-case complexity: O(stones).

### Stone Capture:

- Checks conditions to capture stones. Complexity depends on conditions and stone count. Worst case: O(1) or O(n).

### Game Over Check:

- Checks if all pits for a player are empty. Complexity: O(1) or O(n).

### Declaring Winner:

- Print winner and close the board. Complexity: O(1).

## Key Data Structures:

### Matrices:

- Represent the game board; used to store the visual/image representation of the number of stones in each pit.
- Accessed and modified to visually simulate stone movement.

### Dictionary (board_update method):

- Serves to easily simulate the counterclockwise movement of mancala.
- Helps the visual board representation by translating board_dictionary to respective pits and scores in the matrix.
- Manages the logical state of the board independently of the visual interface.