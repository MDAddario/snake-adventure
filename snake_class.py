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

	elif value == 'dead':
		label.config(bg='purple', relief='raised')
		
	elif value == 'head':
		label.config(bg='green', relief='groove')
		
	else:	# Snake body
		label.config(bg='yellow', relief='groove')

# Contains all game information
class SnakeGame:

	# By default, game inactive
	game_state = 0

	# Constructor
	def __init__(self, board_frame, score_label, args=None):

		self.bind_tk(board_frame, score_label)
		self.set_params(args)
		self.allocate_board()
	
	# Set everything up, ready for play
	def start_game(self):
	
		self.reset_values()
		self.make_board()
		self.make_snake()
		self.make_cherry()
		
	# Attach tkinter elements to object
	def bind_tk(self, board_frame, score_label):
		
		self.board_frame = board_frame
		self.score_label = score_label

	# Set game parameters
	def set_params(self, args):

		# Defaults
		if args is None:
			args = [20,20,6,2]

		self.board_height = args[0]
		self.board_width  = args[1]
		self.snake_init_length  = args[2]
		self.snake_apple_growth = args[3]

	# Values to start the game with
	def reset_values(self):

		# Additional settings
		self.score      = 0
		self.tail_delay = 0
		self.game_state = 1
		self.set_score()
		
	# Allocate memory for the board
	def allocate_board(self):
		
		self.board = np.empty((self.board_height, self.board_width), dtype='object') 
		
		# Generate all grid points
		for i in range(self.board_height):
			for j in range(self.board_width):
				self.board[i, j] = tk.Label(self.board_frame, height=1, width=2)
				self.board[i, j].grid(row=i, column=j)

	# Construct the board
	def make_board(self):

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
	def make_snake(self):
		
		# Randomly generate snake head
		self.head_i = randint(self.snake_init_length, self.board_height - self.snake_init_length - 1)
		self.head_j = randint(self.snake_init_length, self.board_width  - self.snake_init_length - 1)
		configure_label(self.board[self.head_i, self.head_j], 'head')
		
		# Build tail in random direction
		self.last_dir = ['up', 'down', 'left', 'right'][randint(0, 3)]
		
		for k in range(1, self.snake_init_length):

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
		
		# Set default direction
		self.head_dir = self.last_dir
	
	# Spawn the cherry
	def make_cherry(self):

		while True:

			# Spawn at random location not within snake
			i = randint(1, self.board_height - 2)
			j = randint(1, self.board_width  - 2)

			if self.board[i, j].value == 'empty':
				configure_label(self.board[i, j], 'cherry')
				break
	
	# Displace the snake by one tick
	def move_snake(self):
		
		# Prevent 180 spins
		if self.last_dir == 'up' and self.head_dir == 'down':
			self.head_dir = self.last_dir
			
		elif self.last_dir == 'down' and self.head_dir == 'up':
			self.head_dir = self.last_dir
			
		elif self.last_dir == 'left' and self.head_dir == 'right':
			self.head_dir = self.last_dir
			
		elif self.last_dir == 'right' and self.head_dir == 'left':
			self.head_dir = self.last_dir
		
		self.last_dir = self.head_dir
		
		# Grow tail
		if self.tail_delay != 0:
			self.tail_delay -= 1

		# Vanishing tail
		else:
			tail_dir = self.board[self.tail_i, self.tail_j].value
			configure_label(self.board[self.tail_i, self.tail_j], 'empty')

			if tail_dir == 'up':
				self.tail_i -= 1
			elif tail_dir == 'down':
				self.tail_i += 1
			elif tail_dir == 'left':
				self.tail_j -= 1
			elif tail_dir == 'right':
				self.tail_j += 1

		# Advance the head
		configure_label(self.board[self.head_i, self.head_j], self.head_dir)

		if self.head_dir == 'up':
			self.head_i -= 1
		elif self.head_dir == 'down':
			self.head_i += 1
		elif self.head_dir == 'left':
			self.head_j -= 1
		elif self.head_dir == 'right':
			self.head_j += 1

		new_value = self.board[self.head_i, self.head_j].value
		configure_label(self.board[self.head_i, self.head_j], 'head')

		# Cherry capture
		if new_value == 'cherry':

			self.tail_delay += self.snake_apple_growth
			self.score += 1
			self.set_score()
			self.make_cherry()

		# Brutal collision
		elif new_value != 'empty':

			self.game_state = 0
			configure_label(self.board[self.head_i, self.head_j], 'dead')

	def set_score(self):

		self.score_label.config(text='Score = {:d}'.format(self.score))
