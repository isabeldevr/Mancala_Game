from game2dboard import Board
global home_1
global home_2
global current_player
global array

def draw_board():
    """Creates and configures the game board."""
    game = Board(3, 8)  # 3 rows and 8 columns
    game.title = "Mancala"
    game.cell_size = 70
    game.cell_spacing = 60
    game.margin = 0
    game.background_image = "Mankala_board_img"
    if not game.background_image:
        game.cell_color = "bisque"
    game.create_output(background_color="black", color="bisque", font_size=12)
    return game


def start(game):
    """Initializes the game."""
    # Initialize pits with 4 stones each

    array = []
    for row in range(1, 3):
        for col in range(1, 7):
            game[row][col] = 4
            array[row][col] = game[row][col]

    # Set player's cups to 0
    game[1][0] = "Home 1"
    game[2][0] = 0
    game[1][7] = 0
    game[2][7] = "Home 2"

    playing = True

    game.print("Let's play Mancala!")

    while(playing):
        if current_player == 1:
            game.print("Player 1's turn!")
            row, col = mouse_click(btn, row, col)
            if (row, col) == home_1:
                current_player = 2
            else:
                game.print("Invalid move! Try again.")
        else:
            game.print("Player 2's turn!")
            row, col = best_move(game)
            if (row, col) == home_2:
                current_player = 1
            else:
                game.print("Invalid move! Try again.")

        if home_1 > home_2:
            game.print("Player 1 wins!")
            playing = False
        elif home_2 > home_1:
            game.print("Player 2 wins!")
            playing = False
        else:
            game.print("It's a tie!")
            playing = False






def best_move(game):
    """Returns the best move for the current player."""




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
            array[row][col] = game[row][col]

        print(row, col)
        return (row, col)


# Initialize the game
game = draw_board()

# Display the board
game.on_mouse_click = lambda btn, row, col: mouse_click(btn, row, col)
start(game)
game.show()



