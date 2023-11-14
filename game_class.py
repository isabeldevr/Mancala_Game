from game2dboard import Board

ROWS = 4
COLUMNS = 8
CELL_SIZE = 68
CELL_SPACING = 66

class Game:

    def __init__(self):
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
        self.board[1][0] = "\t CPU\n Home Pit"
        self.board[2][0] = 0
        self.board[1][7] = 0
        self.board[2][7] = "\t Player 1\n Home Pit"

        self.current_player = 1
        self.board.print("Let's play Mancala!")


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
        if self.board[row][col] == 0:
            self.board.print("Invalid move! Try again.")
            return None

        if col == 0 or col == 7 or row == 0 or row == 3:
            self.board.print("You cannot click on a home!")
            return None

        if self.current_player == 1 and row != 2:
            self.board.print("Invalid move! Try again.")
        else:
            return self.moving_stones(row, col)

        if self.current_player == 2:
            row, col = self.min_max_ai_player()
            return self.moving_stones(row, col)


    def moving_stones(self, row: int, col: int) -> (int, int):
        """Moves stones around the board"""
        stones = self.board[row][col]
        # remove stones from pit
        self.board[row][col] = 0
        while stones > 0:
            col += 1
            # for counter-clock movement
            if row == 1:
                col -= 2
            # base cases for when we reach the end of the board
            if row == 2 and col == 7:
                row = 1
                col = 6
                self.board[1][7] += 1
                stones -= 1
            if row == 1 and col == 7:
                row = 2
                col = 1
            self.board[row][col] += 1
            stones -= 1
        last_row, last_col = row, col
        if not self.check_game_over():
            self.stone_capture(last_row, last_col)
            self.current_player_update(last_row, last_col)
        ## WE SHOULD ALSO FIND A BETTER TRANSVERSAL METHOD


    def min_max_ai_player(self) -> (int, int):
        current_board_state = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        for row in range(1, 7):
            for col in range(1, 7):
                current_board_state[row][col] = self.board[row][col]
        ## return best row, column
        ## here we can do the min max player
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
        ## REFINE THIS METHOD


    def current_player_update(self, last_row: int, last_col: int) -> None:
        """Updates the current player based on the last move"""
        if last_row == 1 and last_col == 7:
            self.current_player = 1
            self.board.print("Player 1 goes again!")
        elif last_row == 2 and last_col == 7:
            self.current_player = 2
            self.board.print("CPU, Player 2, goes again!")
        else:
            # Switch to the other player's turn
            self.current_player = 3 - self.current_player
            self.board.print("Player " + str(self.current_player) + "'s turn!")
        ## REVISE THIS METHOD


    def check_game_over(self) -> bool:
        "Checks if the game is over and if so declares a winner"
        if all(self.board[1][col] == 0 for col in range(1, 7)):
            self.declare_winner(2)
            return True
        elif all(self.board[2][col] == 0 for col in range(1, 7)):
            self.declare_winner(1)
            return True
        return False


    def declare_winner(self, player: int):
        "This method declares the winner"
        if player == 1:
            self.board.print("Player 1 wins!")
        else:
            self.board.print("CPU wins!")
        ## ADD LINK TO RE-START OR QUIT FUNCTION

## SOME NOTES

# 1. We need to implement the min max player
# 2. We need to fix the quit button (so u can quit at any time) + at the end of th game
# 3. We need to fix the restart button
# 4. We need to refine the stone capture method (look at how they did in YT Video)
# 5. We need to refine the transveral method (look at how they did in YT Video)
# 6. We need to refine the player update mtehod (not updating properly idk why)
