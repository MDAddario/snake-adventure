import numpy as np
import tkinter as tk
from random import randint

# Stylize board squares based off their value
def configure_label(label, value):
	
	label.value = value
	
	if value == 'wall':
		label.config(bg='black', relief='raised')
		
	elif value == 'empty':
		label.config(bg='white', relief='groove')
		
	elif value == 'cherry':
		label.config(bg='red', relief='raised')
		
	else:	# Snake body
		label.config(bg='yellow', relief='groove')

# Contains all game information
class SnakeGame:

	def __init__(self, tk_args, param_args=None):
		
		self.bind_tk(tk_args)
		self.init_params(param_args)
		self.init_board()
		self.init_snake()
		self.init_cherry()
		
	# Attach tkinter elements to object
	def bind_tk(self, tk_args):
		
		self.board_frame = tk_args[0]
		self.score_label = tk_args[1]

	# Set game parameters
	def init_params(self, args):

		# Defaults
		if args is None:
			args = [6,6,3,1]

		self.board_height = args[0]
		self.board_width  = args[1]
		self.snake_init_length  = args[2]
		self.snake_apple_growth = args[3]

		# Additional settings
		self.score      = 0
		self.tail_delay = 0
		self.game_state = 0

	# Construct the board
	def init_board(self):

		'''
		Possible board values:
		'wall'   : Wall
		'empty'  : Empty
		'cherry' : Cherry
		'head'   : Snake head
		'up'     : Snake body, direction up
		'down'   : Snake body, direction down
		'left'   : Snake body, direction left
		'right'  : Snake body, direction right
		'''

		self.board = np.empty((self.board_height, self.board_width), dtype='object') 
		
		# Generate all grid points
		for i in range(self.board_height):
			for j in range(self.board_width):
				self.board[i, j] = tk.Label(self.board_frame, height=1, width=2)
				self.board[i, j].grid(row=i, column=j)
		
		# Empty all squares
		for i in range(self.board_height):
			for j in range(self.board_width):
				configure_label(self.board[i, j], 'empty')

		# Build the wall
		for i in range(self.board_height):
			configure_label(self.board[i,                    0], 'wall')
			configure_label(self.board[i, self.board_width - 1], 'wall')

		for j in range(self.board_width):
			configure_label(self.board[                    0, j], 'wall')
			configure_label(self.board[self.board_height - 1, j], 'wall')

	# Construct the snake
	def init_snake(self):
		
		# Randomly generate snake head
		self.head_i = randint(self.snake_init_length, self.board_height - self.snake_init_length - 1)
		self.head_i = randint(self.snake_init_length, self.board_width  - self.snake_init_length - 1)
		configure_label(self.board[self.head_i, self.head_j], 'head')
		
		# Build tail in random direction
		self.last_dir = ['up', 'down', 'left', 'right'][randint(0, 3)]
		
		for k in range(1, snake_init_length):

			if self.last_dir == 'up':
				self.tail_i = self.head_i + k
				self.tail_j = self.head_j
			
			elif self.last_dir == 'down':
				self.tail_i = self.head_i - k
				self.tail_j = self.head_j
			
			elif self.last_dir == 'left':
				self.tail_i = self.head_i
				self.tail_j = self.head_j + k
			
			elif self.last_dir == 'right':
				self.tail_i = self.head_i
				self.tail_j = self.head_j - k
			
			configure_label(self.board[self.tail_i, self.tail_j], self.last_dir)
	
	# Spawn the cherry
	def init_cherry(self):

		while True:

			# Spawn at random location not within snake
			i = randint(1, board_height - 2)
			j = randint(1, board_width  - 2)

			if self.board[i, j].value == 'e':
				configure_label(self.board[i, j], 'cherry')
				break
	
	# Displace the snake by one tick
	def move_snake(self, input_dir):
		
		# Prevent 180 spins
		if self.last_dir == 'up' and input_dir == 'down':
			head_dir = self.last_dir
			
		elif self.last_dir == 'down' and input_dir == 'up':
			head_dir = self.last_dir
			
		elif self.last_dir == 'left' and input_dir == 'right':
			head_dir = self.last_dir
			
		elif self.last_dir == 'right' and input_dir == 'left':
			head_dir = self.last_dir
			
		else:
			head_dir = input_dir
			
		self.last_dir = head_dir
			
		# Grow tail
		if self.tail_delay != 0:
			self.tail_delay -= 1

		# Vanishing tail
		else:
			tail_dir = self.board[self.tail_i, self.tail_j].value
			configure_label(self.board[self.tail_i, self.tail_j], 'empty')

			if tail_dir == 'u':
				self.tail_i -= 1
			elif tail_dir == 'd':
				self.tail_i += 1
			elif tail_dir == 'l':
				self.tail_j -= 1
			elif tail_dir == 'r':
				self.tail_j += 1

		# Advance the head
		configure_label(self.board[self.head_i, self.head_j], head_dir)

		if head_dir == 'u':
			self.head_i -= 1
		elif head_dir == 'd':
			self.head_i += 1
		elif head_dir == 'l':
			self.head_j -= 1
		elif head_dir == 'r':
			self.head_j += 1

		new_value = self.board[self.head_i, self.head_j].value
		configure_label(self.board[self.head_i, self.head_j], 'head')

		# Cherry capture
		if new_value == 'c':

			self.tail_delay += self.snake_apple_growth
			self.score += 1
			self.init_cherry()

		# Brutal collision
		elif new_value != 'e':

			self.game_state = 0

# The main attraction
if __name__ == '__main__':
	
	game = SnakeGame()