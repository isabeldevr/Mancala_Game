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
            # vvv SOMETHING IN THIS WHILE LOOP IS CRASHING THE GAME vvv
        #while value > 0:
        #    col = (col + 1) % 7  # Wrap around to the start
        #    if (row == 0 and col != 6) or (row == 1 and col != 0):
        #        game[row][col] += 1
        #        value -= 1
        
def start():
    game[1][0] = game[2][0] = 0  # Player 1's cup
    game[1][7] = game[2][7] = 0  # Player 2's cup
    for row in range(1, 3):
        for col in range(1, 7):
            game[row][col] = 4  # 4 stones in each pit
    game.print("Let's play Mancala!")
    

### CREATING THE BOARD ###
game = Board(4, 8)
game.title = "Mancala"
game.cell_size = 90
game.cell_spacing = 40
game.margin = 0
game.background_image = "mancala_board.png"
if not game.background_image:
    game.cell_color = "bisque"
game.on_mouse_click = mouse_click
game.on_key_press = key_press
game.on_start = start
game.create_output(background_color="#606163",
                   color="white",
                   font_size=12)
game.show()