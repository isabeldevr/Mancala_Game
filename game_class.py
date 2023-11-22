from game2dboard import Board

ROWS = 4
COLUMNS = 8
CELL_SIZE = 117
CELL_SPACING = 10

# INVALID_ROWS = [0,3]  # Might not be needed, we can just do "not in CUP_ROWS"
P1_ROW = 2
P1_COL = 7
P2_ROW = 1
P2_COL = 0
CUP_ROWS = [P2_ROW, P1_ROW]
HOME_COLUMNS = [P2_COL,P1_COL]
CUP_COLUMNS = range(1,7)  #[1,2,3,4,5,6]


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

        #self.board_slots = {i: 4 for i in range(1, 13)}



    def start(self) -> None:
        """Initializes the game."""

        self.p2_type = 0  # Default Player 2 type is HUMAN

        for row in range(1, 3):  # Initialize pits with 4 stones each
            for col in range(1, 7):
                self.board[row][col] = 4

        # Set player's cups to 0
        self.board[1][0] = 0
        self.board[2][0] = "Player 2\nHome Pit"
        self.board[1][7] = "Player 1\nHome Pit"
        self.board[2][7] = 0

        self.current_player = 1
        self.board.print(f"Let's play Mancala! Player {self.current_player}, goes first!")

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


    def draw_board(self) -> None:
        """Draws the board"""
        self.board.show()


    def mouse_click(self, btn, row: int, col: int):
        """Handles mouse clicks"""
        if row not in CUP_ROWS:
            return None

        if (col in HOME_COLUMNS) and (row in CUP_ROWS):
            self.board.print("You cannot click on a home!")
            return None

        if self.current_player == 1:
            if row != P1_ROW:
                self.board.print("This cup belongs to Player 2!\nTry again.")
                return None
            if self.board[row][col] == 0:
                self.board.print("This cup is empty!\nTry again.")
                return None
            self.board.print("")
            return self.moving_stones(row, col)

        if self.current_player == 2:
            # if self.p2_type == 1:
                # self.p2_ai(row, col)
            if row != P2_ROW:
                self.board.print("This cup belongs to Player 1!\nTry again.")
                return None
            if self.board[row][col] == 0:
                self.board.print("This cup is empty!\nTry again.")
                return None
            self.board.print("")
            return self.moving_stones(row, col)


    def moving_stones(self, row: int, col: int) -> (int, int):
        """Moves stones around the board"""
        tempStones = self.board[row][col]
        self.board[row][col] = 0  # remove stones from pit

        while tempStones > 0:
            if row == P1_ROW:  # clockwise movement
                col += 1
            else:  # counter-clock movement
                col -= 1

            if (row == P1_ROW) and (col == P1_COL):  # reach the end of the RIGHT side
                self.board[P1_ROW][P1_COL] += 1
                row = P2_ROW
                col = P1_COL - 1
                tempStones -= 1
            if (row == P2_ROW) and (col == P2_COL):  # reach the end of the LEFT side
                self.board[P2_ROW][P2_COL] += 1
                row = P1_ROW
                col = P2_COL + 1
                tempStones -= 1
            self.board[row][col] = int(self.board[row][col]) + 1
            tempStones -= 1

        last_row, last_col = row, col
        if not self.check_game_over():
            #self.stone_capture(last_row, last_col)
            self.current_player_update(last_row, last_col)

        ## WE SHOULD ALSO FIND A BETTER TRANSVERSAL METHOD


    def p2_ai(self) -> (int, int):
        current_board_state = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        for row in range(1, 7):
            for col in range(1, 7):
                current_board_state[row][col] = self.board[row][col]
        # return best row, column
        # here we can do the min max player
        return None


    def stone_capture(self, last_row: int, last_col: int) -> None:
        """Checks if we can capture stones"""
        if (last_row == 1) and (self.board[last_row][last_col] == 1) and (self.board[2][last_col] != 0):
            self.board[1][7] += self.board[2][last_col] + 1
            self.board[2][last_col] = 0
            self.board[1][last_col] = 0
        elif (last_row == 2) and (self.board[last_row][last_col] == 1) and (self.board[1][last_col] != 0):
            self.board[2][7] += self.board[1][last_col] + 1
            self.board[1][last_col] = 0
            self.board[2][last_col] = 0
        else:
            pass
        # REFINE THIS METHOD


    def current_player_update(self, last_row: int, last_col: int) -> None:
        """Updates the current player based on the last move"""
        if last_row == 1 and last_col == 7: # P1 lands on home cup
            self.current_player = 1
            self.board.print("Player 1 goes again!")
        elif last_row == 2 and last_col == 7: # P2 lands on home cup
            self.current_player = 2
            self.board.print("Player 2 goes again!")
        else:
            # Switch to the other player's turn
            self.current_player = 3 - self.current_player
            self.board.print(f"Player {str(self.current_player)}'s turn!")
        # REVISE THIS METHOD


    def check_game_over(self) -> bool:
        """Checks if the game is over and if so declares a winner"""
        if all(self.board[1][col] == 0 for col in CUP_COLUMNS):
            self.declare_winner(2)
            return True
        elif all(self.board[2][col] == 0 for col in CUP_COLUMNS):
            self.declare_winner(1)
            return True
        return False


    def declare_winner(self, player: int) -> None:
        """This method declares the winner"""
        if player == 1:
            self.board.print("Player 1 wins!")
        else:
            self.board.print("Player 2 wins!")
        # for now we close the board when finished
        self.board.close()
        # ADD LINK TO RE-START OR QUIT FUNCTION


if __name__ == "__main__":
    game = Game()
    game.start()
    game.draw_board()


## SOME NOTES
# 1. Implement the min max player
# 2. Fix the quit + restart button (so u can quit/restart at any time) + at the end of th game
# 3. Refine the stone capture method (look at how they did in YT Video)
# 4. Refine the transveral method (look at how they did in YT Video)
# 5. Adjust the player update method (so that u cant clik outside your turn) + sometimes message not showing
# 6. Add the stone images to the board
