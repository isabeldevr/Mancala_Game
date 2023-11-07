from game2dboard import Board

### CREATING THE BOARD ###
game = Board(4, 8)
game.cell_size = 90
game.cell_spacing = 40
game.background_image = "mancala_board_5.png"
if not game.background_image:
    game.cell_color = "bisque"
game.title = "Mancala"


# create the home pits
game[1][0] = game[2][0] = "H"  # Player 1's cup
game[1][7] = game[2][7] = "H"  # Player 2's cup


### STARTING THE GAME ###
for row in range(1, 3):
    for col in range(1, 7):
        game[row][col] = 4  # 4 stones in each pit

## click not working
def mouse_click(row, col):
    if game[row][col] == 0 or (row == 0 and col == 0) or (row == 1 and col == 0) or (row == 0 and col == 6) or (row == 1 and col == 6):
        print("Invalid click on this cell!")
    else:
        value = game[row][col]
        game[row][col] = 0
        while value > 0:
            col = (col + 1) % 7  # Wrap around to the start
            if (row == 0 and col != 6) or (row == 1 and col != 0):
                game[row][col] += 1
                value -= 1

# Show the board
game.show()