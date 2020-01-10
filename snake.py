# Import the champions
import numpy as np
import tkinter as tk
from random import randint
from snake_class import SnakeGame

# Tkinter management
root = tk.Tk()
root.title("Snake Adventure")
board_frame = tk.Frame(root)
board_frame.pack()
lower_frame = tk.Frame(root)
lower_frame.pack()

# Score display
score_label = tk.Label(lower_frame, relief='groove')
score_label.pack()

# Generate the game object
game = SnakeGame(board_frame, score_label)

# Keyboard inputs
def upKey(event):
	game.head_dir = 'up'

def downKey(event):
	game.head_dir = 'down'
	
def leftKey(event):
	game.head_dir = 'left'

def rightKey(event):
	game.head_dir = 'right'

board_frame.bind('<Up>', upKey)
board_frame.bind('<Down>', downKey)
board_frame.bind('<Left>', leftKey)
board_frame.bind('<Right>', rightKey)
board_frame.focus_set()

# Progress one game tick
def update_board():

	# Make sure game is active
	if not game.game_state:
		return

	# Schedule next game tick
	root.after(40, update_board)
	
	# Move the snake
	game.move_snake()

# Game control system
def start():

	# Only begin a new game if current game inactive
	if game.game_state:
		return
	
	# Start game
	game.start_game()
	update_board()

start_button = tk.Button(lower_frame, text="Start Game", relief='groove', \
						command=start, bg='black', fg='white')
start_button.pack()

root.mainloop()
