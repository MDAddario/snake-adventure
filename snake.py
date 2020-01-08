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

def set_score(score):
	score_label.config(text='Score = {:d}'.format(score))

# Progress one game tick
def update_board():

	# Make sure game is active
	if not game_state:
		return

	# Schedule next game tick
	root.after(40, update_board)
	
	# Move the snake

# Keyboard inputs
def upKey(event):
	global direction
	direction = 'i'

def downKey(event):
	global direction
	direction = 'd'
	
def leftKey(event):
	global direction
	direction = 'l'

def rightKey(event):
	global direction
	direction = 'r'

board_frame.bind('<Up>', upKey)
board_frame.bind('<Down>', downKey)
board_frame.bind('<Left>', leftKey)
board_frame.bind('<Right>', rightKey)
board_frame.focus_set()

# Game control system
def start():

	# Only begin a new game if current game inactive
	if game_state:
		return

	game_state = 1
	
	update_board()

start_button = tk.Button(lower_frame, text="Start Game", relief='groove', \
						command=start, bg='black', fg='white')
start_button.pack()

root.mainloop()
