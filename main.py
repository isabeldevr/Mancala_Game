from game2dboard import Board

### CREATING THE BOARD ###
game = Board(2, 7)
game.cell_size = 127
game.cell_spacing = 9.5
game.background_image = "Mancala_board_img.png"
game.title = "Mancala Board"


# create the home pits
game[0][0] = game[1][0] = "H"  # Player 1's home
game[0][6] = game[1][6] = "H"  # Player 2's home


### STARTING THE GAME ###
for row in range(2):
    for col in range(1, 6):
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
