from game2dboard import Board
import random
import copy


ROWS = 4
COLUMNS = 8
CELL_SIZE = 117
CELL_SPACING = 10
PLAYER_1 = 1
PLAYER_2 = 2
STONE_IMAGE_FILES = [f"{i}.png" for i in range(0, 48)]
# TOMAS: 48 is the maximum stones u could ever have, so we need up to 48 this sucks so sorry

class MancalaGame:

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
        self.board_dictionary = {}
        self.board.cursor = "arrow"

    def start(self) -> None:
        """Initializes the game.
        input: None
        output: None. Calls the draw_board method with the initial board"""

        # Initialise the UI
        self.initialise_board_ui()

        # Initialising the player: human player goes first
        self.current_player = 2
        self.board.print(f"Let's play Mancala! \t Player {self.current_player}, goes first!")

        # Initialise the board dictionary
        self.board_dictionary = {
            "Row_1": [4, 4, 4, 4, 4, 4],
            "Row_2": [4, 4, 4, 4, 4, 4],
            "Player1_score": 0,
            "Player2_score": 0,
        }

    def initialise_board_ui(self):
        """We initialise the state of the board's user interface
        input: None
        output: None """
        for row in range(1, 3):
            for col in range(1, 7):
                self.board[row][col] = 4

            # Set player's cups to 0
        self.board[1][0] = "Player 1"
        self.board[2][0] = 0
        self.board[1][7] = 0
        self.board[2][7] = "Player 2, You"

    def keyboard_command(self, key) -> None:
        """Handle quitting and re-start of game
        input: key pressed
        output: None. Calls the start or quit method"""
        if key == "q":
            self.board.close()
        elif key == "r":
            self.board.clear()
            self.start()

    def draw_board(self) -> None:
        """Draws the board"""
        self.board.show()

    def mouse_click(self, btn: int, row: int, col: int) -> None:
        """Handles mouse clicks
        input: btn, row clicked, col clicked
        output: None. Calls the moving_stones method"""
        if self.current_player == PLAYER_1:
            return None

        if self.board[row][col] == 0 or row != 2 or col in {0, 7} or row in {0, 3}:
            self.board.print("Invalid move! Try again.")
            return None

        self.board.print("")
        self.moving_stones(row, col)

    def moving_stones(self, row: int, col: int) -> None:
        """Moves stones around the board:
        input: row of chosen cell, column  of chosen cell
        output: None. Calls the board_update method """
        start_row = row
        col -= 1
        start_col = col
        stones = self.board_dictionary[f"Row_{self.current_player}"][col]

        # Remove stones from pit
        self.board_dictionary[f"Row_{row}"][col] = 0

        while stones > 0:
            # Move to the next column
            col += 1
            # Check if we reached the end of the row
            if col >= len(self.board_dictionary[f"Row_{row}"]):
                self.board_dictionary[f"Player{self.current_player}_score"] += 1
                print(self.board_dictionary[f"Player{self.current_player}_score"])
                row = 3 - row
                col = 0
                stones -= 1

            else: # Update the count of stones in the current cell
                self.board_dictionary[f"Row_{row}"][col] += 1
                stones -= 1

        # Check if game over
        last_row, last_col = row, col
        continue_game = self.check_game_over()

        # If game can continue
        if not continue_game:
            self.stone_capture(start_row, start_col, last_row, last_col, self.board_dictionary)
            self.current_player_update(last_row, last_col)

        # Update the board
        return self.board_update(self.board_dictionary)

    def board_update(self, board_dictionary: dict) -> None:
        """Updates the board
        input: board_dictionary
        output: None"""
        for col in range(1, 7):
            self.board[1][COLUMNS - col - 1] = board_dictionary["Row_1"][col - 1]
            self.board[2][col] = board_dictionary["Row_2"][col - 1]
        self.board[1][7] = board_dictionary["Player2_score"]
        self.board[2][0] = board_dictionary["Player1_score"]

    def ai_player(self) -> (int, int):
        """This method is the AI player
        input: None
        output: best move coordinates (row, col)"""
        return self.make_best_move(self.current_player, 1)

    def make_best_move(self, player_to_evaluate, depth) -> (int, int):
        """This method makes the best move
        input: player_to_evaluate, depth
        output: best move (row, col)"""

        # base case to stop recursion
        if depth <= 0:
            return random.choice(self.possible_moves_by_player(player_to_evaluate))

        possible_moves = self.possible_moves_by_player(player_to_evaluate)
        if possible_moves:
            # Evaluate each move and choose the one with the highest score
            best_move = max(possible_moves, key=lambda move: self.evaluate_move(move, depth=depth-1))
            print(best_move)
            return best_move[0], best_move[1]

    def possible_moves_by_player(self, player_to_evaluate) -> list:
        """This method returns the possible moves by player
        input: player_to_evaluate
        output: list"""
        values = []
        for col in range(6):
            values.append((player_to_evaluate, col))
        return values

    def evaluate_move(self, move, depth) -> int:
        """ This method evaluates the move
        input: move, depth of recursion
        output: points obtained for the move"""
        dictionary_copy = copy.deepcopy(self.board_dictionary)
        points = 0
        stones = dictionary_copy[f"Row_{self.current_player}"][move[1]]

        # remove stones from pit
        dictionary_copy[f"Row_{self.current_player}"][move[1]] = 0
        row = self.current_player
        col = move[1]

        while stones > 0:
            # Move to the next column
            col += 1
            # Check if we reached the end of the row
            if col >= len(dictionary_copy[f"Row_{row}"]):
                dictionary_copy[f"Player{self.current_player}_score"] += 1
                points += 1
                row = 3 - row
                col = 0
                stones -= 1
            # Update the count of stones in the current cell
            else:
                dictionary_copy[f"Row_{row}"][col] += 1
                stones -= 1

        # check if we capture stones
        last_row, last_col = row, col
        self.stone_capture(move[0], move[1], last_row, last_col, dictionary_copy)

        if depth > 0:
            opponent_moves = self.make_best_move(3 - self.current_player, depth - 1)
            points -= self.evaluate_move(opponent_moves, depth - 1)
        return points

    def stone_capture(self, start_row: int, start_col: int, last_row: int, last_col: int, dictionary: dict) -> None:
        """ Checks if we can capture stones by checking if we land in an empty pit on our side
        input: starting row, starting column, last row, last column, dictionary
        output: None """
        if start_row == last_row and start_col != last_col and dictionary[f"Row_{last_row}"][last_col] == 1:
            dictionary[f"Row_{last_row}"][last_col], dictionary[f"Row_{3 - last_row}"][last_col] = \
                dictionary[f"Row_{last_row}"][last_col], dictionary[f"Row_{3 - last_row}"][last_col]
        return self.board[last_row][last_col]

    def current_player_update(self, last_row: int, last_col: int) -> None:
        """Updates the current player based on the last move
        input: last row, last column
        output: None"""
        if last_row == 2 and last_col == 6:
            self.current_player = PLAYER_1
            self.board.print("Player 1 goes again!")
        elif last_row == 1 and last_col == 0:
            self.current_player = PLAYER_2
            self.board.print("You can go again!")
            self.board.cursor = "arrow"
        else:
            self.current_player = 3 - self.current_player

        # Move the following line outside the if condition
        self.board.print("Player {}'s turn".format(self.current_player))

        if self.current_player == 1:
            self.cursor = None
            row, col = self.ai_player()
            return self.moving_stones(row, col + 1)

    def check_game_over(self) -> bool:
        """Checks if the game is over and if so declares a winner. First to finish is always the winner.
        input: None
        output: bool"""
        for row in range(1, 3):
            if self.board_dictionary[f"Row_{row}"] == [0, 0, 0, 0, 0, 0] and self.board_dictionary[f"Player{row}_score"] > self.board_dictionary[f"Player{3-row}_score"]:
                print("we are here")
                return self.declare_winner(row)
        return False

    def declare_winner(self, player: int) -> bool:
        """This method declares the winner
        input: first player to finish
        output: bool"""
        self.board.cursor = None
        self.board.print(f"Player {player} wins! Congratulations! \n Press 'r' to restart or 'q' to quit")
        return True


# SOME NOTES
# current player revise method (turns are a bit wonky, its not easy to see who is playing i want to introduce a delay )
# Ask teacher what kind of dosc-strings he prefers
# Handle draws
# 6. We need to add the stone images to the board (so layer the stones instead of the numbers)
#      -> `create a method for ths and put images into a list access according to necessity
# 7.   Optimise the code (make it more efficient) where it says revise
#  8. make so that u cannot land in opponents points (just make sure)
