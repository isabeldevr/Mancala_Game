from game2dboard import Board

global home_1
global home_2
global current_player

def draw_board():
    """Creates and configures the game board."""
    game = Board(3, 8)  # 3 rows and 8 columns
    game.title = "Mancala"
    game.cell_size = 90
    game.cell_spacing = 40.8
    game.margin = 0
    game.background_image = "mancala_board.png"
    if not game.background_image:
        game.cell_color = "bisque"
    return game


def start(game):
    """Initializes the game."""
    # Initialize pits with 4 stones each
    for row in range(1, 3):
        for col in range(1, 7):
            game[row][col] = 4

    # Set player's cups to 0
    game[1][0] = "Home 1"
    game[2][0] = 0
    game[1][7] = 0
    game[2][7] = "Home 2"

    current_player = 1
    game.print("Let's play Mancala!")


def mouse_click(btn, row, col):
    """Handles mouse click events on cells or cups."""
    if col == 0 or col == 7 or row == 0 or row == 3:
        game.print("Invalid click on this cell / cup!")
        return
    elif game[row][col] == 0:
        game.print("No stone!")
        return
    else:
        value = game[row][col]
        game[row][col] = 0

        for i in range(value):
            if row == 1 and col != 0:
                col = (col - 1) % 8
            elif row == 2 and col != 0:
                col = (col + 1) % 8
            if row == 1 and col == 0:
                row = 2
            elif row == 2 and col == 7:
                row = 1
            game[row][col] += 1

        print(row, col)
        return (row, col)


# playing the game
def playing_mancala(game):
   while home_1 < 24 and home_2 < 24:
       if current_player == 1:
           game.print("Player 1's turn!")
           row, col = mouse_click(btn, row, col)
           if (row, col) == home_1:
               current_player = 2
           else:
               game.print("Invalid move! Try again.")
       else:
           game.print("Player 2's turn!")
           row, col = mouse_click(btn, row, col)
           if (row, col) == home_2:
               current_player = 1
           else:
               game.print("Invalid move! Try again.")

   if home_1 > home_2:
       game.print("Player 1 wins!")
   elif home_2 > home_1:
       game.print("Player 2 wins!")
   else:
       game.print("It's a tie!")


# Initialize the game
game = draw_board()

# Display the board
game.create_output(background_color="black", color="bisque", font_size=12)
game.on_mouse_click = lambda btn, row, col: mouse_click(btn, row, col)
start(game)
game.show()


