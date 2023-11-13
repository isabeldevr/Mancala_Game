from game2dboard import Board

ROWS = 4
COLUMNS = 8
CELL_SIZE = 70
CELL_SPACING = 60

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
        self.board.on_key_press = self.keyboard_command

    def start(self) -> None:
        """Initializes the game."""

        # Initialize pits with 4 stones each
        self.array = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        for row in range(1, 3):
            for col in range(1, 7):
                self.board[row][col] = 4
                self.array[row][col] = self.board[row][col]

        # Set player's cups to 0
        self.board[1][0] = "Home 1"
        self.board[2][0] = 0
        self.board[1][7] = 0
        self.board[2][7] = "Home 2"

        self.current_player = 1
        ## SEE WHERE WE CAN UPDATE
        self.board.print("Let's play Mancala!")

    def keyboard_command(self, event) -> None:
        """Handle start of game"""
        if event.key == "q":
            self.board.close()
        elif event.key == "r":
            self.board.clear()
            self.start()

    def draw_board(self) -> None:
        self.board.show()

    def mouse_click(self, row: int, col: int) -> (int, int):
        if self.board[row][col] == 0:
            self.board.print("Invalid move! Try again.")
            return None

        if self.board[2][0] or self.board[1][7] or self.board[2][7] or self.board[1][0]:
            self.board.print("You cannot click on a home!")
            return None

        else:
            if self.current_player == 1:
                return self.moving_stones(row, col)
            else:
                return self.min_max_ai_player()


    def moving_stones(self, row: int, col: int) -> (int, int):
        if self.current_player == 1:
            stones = self.board[row][col]
            while stones > 0:
                for row in range(2, 0, -1):
                    for col in range(6, 0, -1):
                        self.array[row][col] -= 1
                        self.board[row][col] = self.array[row][col]
                        stones -= 1
        else:
            ## this has to connect to min max in some way
            stones = self.board[row][col]
            while stones > 0:
                for row in range(1, 3):
                    for col in range(1, 7):
                        self.array[row][col] -= 1
                        self.board[row][col] = self.array[row][col]
                        stones -= 1
        last_row, last_col = row, col
        self.current_player_update(last_row, last_col)
        self.check_game_over()
        ## here maybe we can add a function that checks if the game is over (and if not update the current player?)

    def min_max_ai_player(self):
        pass
        # return row, column?
        # here we can do the min max player

    def current_player_update(self, last_row: int, last_col: int):
        pass
        ## here we can update the current player based on the last move

    def check_game_over(self):
        pass
        ## here we can check if the game is over and if so declare a winner



