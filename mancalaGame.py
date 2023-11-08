from game2dboard import Board

def key_press(key):
    if key == "r":
        start()

def mouse_click(btn, row, col):
    if col == 0 or col == 7 or row == 0 or row == 3:
        game.print("Invalid click on this cell / cup!")
        return
    else:
        value = game[row][col]
        game[row][col] = 0

        while value > 0:
            # fixed the "col" wrap around from 7 to 8 to match the number of columns
            col = (col + 1) % 8  # Wrap around to the start (you have 8 columns)
            if (row == 1 and col != 0) or (row == 2 and col != 7):
                game[row][col] += 1
                value -= 1

def start():
    for row in range(1, 3):
        for col in range(1, 7):
            game[row][col] = 4  # 4 stones in each pit

    # Set player's cups to 0
    game[1][0] = game[2][0] = 0
    game[1][7] = game[2][7] = 0

    game.print("Let's play Mancala!")

# CREATING THE BOARD
game = Board(3, 8)  # 3 rows and 8 columns
game.title = "Mancala"
game.cell_size = 90
game.cell_spacing = 40
game.margin = 0
game.background_image = "mancala_board.png"
if not game.background_image:
    game.cell_color = "bisque"

# Initialize the game
start()

# Display the board
game.create_output(background_color="#606163", color="white", font_size=12)
game.on_mouse_click = mouse_click
game.on_key_press = key_press
game.show()
