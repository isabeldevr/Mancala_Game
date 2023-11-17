from game2dboard import Board

ROWS = 4
COLUMNS = 8
CELL_SIZE = 68
CELL_SPACING = 66


class Game:

    def __init__(self):
        self.current_player = None
        self.board = Board(ROWS, COLUMNS)
        self.board.title = "Mancala"
        self.board.cell_size = CELL_SIZE
        self.board.cell_spacing = CELL_SPACING
        self.board.margin = 0
        self.board.background_image = "mancala_board.png"
        if not self.board.background_image:
            self.board.cell_color = "bisque"
        self.board.create_output(background_color="black", color="bisque", font_size=12)
        self.board.on_start = self.start
        self.board.on_key_press = self.keyboard_command
        self.board.on_mouse_click = self.mouse_click

    def start(self) -> None:
        """Initializes the game."""
        # Initialize pits with 4 stones each
        for row in range(1, 3):
            for col in range(1, 7):
                self.board[row][col] = 4

        # Set player's cups to 0
        self.board[1][0] = "\t Player 1 CPU\n Home Pit"
        self.board[2][0] = 0
        self.board[1][7] = 0
        self.board[2][7] = "\t Player 2\n Home Pit"

        # Initialising the player
        self.current_player = 2
        self.board.print(f"Let's play Mancala! \t Player {self.current_player}, goes first!")

        ## Initialise the board dictionary
        ## This is what we
        self.board_dictionary = {
            "Row_1": [4, 4, 4, 4, 4, 4],
            "Row_2": [4, 4, 4, 4, 4, 4],
            "Player1_score": 0,
            "Player2_score": 0,
        }

    def keyboard_command(self, key) -> None:
        """Handle start of game"""
        if key == "q":
            self.board.close()
        elif key == "r":
            self.board.clear()
            self.start()
        ## REVISE THIS METHOD

    def draw_board(self) -> None:
        """Draws the board"""
        self.board.show()

    def mouse_click(self, btn: int, row: int, col: int) -> (int, int):
        """Handles mouse clicks"""
        if self.current_player == 1:
            self.board.print("It is not your turn! Player 1 (CPU) is playing")
            self.moving_stones(*self.ai_player())
            return None

        if self.board[row][col] == 0 or row != 2 or col in {0, 7} or row in {0, 3}:
            self.board.print("Invalid move! Try again.")
            return None

        self.board.print("")
        return self.moving_stones(row, col)

    def moving_stones(self, row: int, col: int) -> (int, int):
        """Moves stones around the board"""
        col -= 1
        stones = self.board_dictionary[f"Row_{self.current_player}"][col]
        # remove stones from pit
        self.board_dictionary[f"Row_{self.current_player}"][col] = 0
        row = self.current_player

        while stones > 0:
            # Move to the next column
            col += 1

            # Check if we reached the end of the row
            if col >= len(self.board_dictionary[f"Row_{row}"]):
                self.board_dictionary[f"Player{self.current_player}_score"] += 1
                row = 3 - row
                col = 0

            # Update the count of stones in the current cell
            self.board_dictionary[f"Row_{row}"][col] += 1
            stones -= 1

        self.board_update(self.board_dictionary)
        last_row, last_col = row, col
        continue_game = self.check_game_over()
        if not continue_game:
            self.stone_capture(last_row, last_col)
            self.current_player_update(last_row, last_col)

    def board_update(self, board_dictionary: dict) -> None:
        """Updates the board"""
       ## make it so that this updates the board correctly
        for col in range(1, 7):
            self.board[1][COLUMNS-col-1] = board_dictionary["Row_1"][col - 1]
            self.board[2][col] = board_dictionary["Row_2"][col - 1]
        self.board[1][7] = board_dictionary["Player1_score"]
        self.board[2][0] = board_dictionary["Player2_score"]
        # put the update images function here or integrate
        # use an array [0, 1, 2, 3, 4, 5, 6] to access the correct images

    def ai_player(self) -> (int, int):
        """This method is the AI player"""
        # we can use heap and priority queues
        pass

    def stone_capture(self, last_row: int, last_col: int) -> None:
        """Checks if we can capture stones"""
        if last_row == 1 and self.board[last_row][last_col] == 1 and self.board[2][last_col] != 0:
            self.board[1][7] += self.board[2][last_col] + 1
            self.board[2][last_col] = 0
            self.board[1][last_col] = 0
        elif last_row == 2 and self.board[last_row][last_col] == 1 and self.board[1][last_col] != 0:
            self.board[2][7] += self.board[1][last_col] + 1
            self.board[1][last_col] = 0
            self.board[2][last_col] = 0
        else:
            pass
        # REFINE THIS METHOD

    def current_player_update(self, last_row: int, last_col: int) -> None:
        """Updates the current player based on the last move"""
        # string = "Player " + str(self.current_player) + "'s turn!" if self.current_player == 1 else "CPU, Player 2, goes again!"
        if last_row == 1 and last_col == 7:
            self.current_player = 1
            self.board.print("Player 1, CPU goes again!")
        elif last_row == 2 and last_col == 7:
            self.current_player = 2
            self.board.print("Player 2, goes again!")
        else:
            # Switch to the other player's turn
            self.current_player = 3 - self.current_player
            self.board.print("Player " + str(self.current_player) + "'s turn!")
        # REVISE THIS METHOD

    def check_game_over(self) -> bool:
        """Checks if the game is over and if so declares a winner"""
        if all(self.board[1][col] == 0 for col in range(1, 7)):
            self.declare_winner(1)
            return True
        elif all(self.board[2][col] == 0 for col in range(1, 7)):
            self.declare_winner(2)
            return True
        return False

    def declare_winner(self, player: int) -> None:
        """This method declares the winner"""
        self.board.print(f"Player{player} wins!")
        # ADD LINK TO RE-START OR QUIT FUNCTION

## SOME NOTES
# 1. We need to implement the min max, trees player
# 2. We need to fix the quit + restart button (so u can quit/restart at any time) + at the end of th game
# 3. We need to refine the stone capture method (look at how they did in YT Video)
# 4. We need to refine the transveral method (look at how they did in YT Video)
# 5. We need to adjust the player update method (so that u cant clik outside your turn) + sometimes message not showing
# 6. We need to add the stone images to the board (so layer the stones instead of the numbers)
#      -> `create a method for ths and put images into a list access according to necessity

