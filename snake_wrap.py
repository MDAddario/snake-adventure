import numpy as np
from random import randint

# Contains all game information
class SnakeGame:

	def __init__(self, args=None):
		
		self.init_params(args)
		self.init_board()
		self.init_snake()
		self.init_cherry()

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
		self.game_state = 1

	# Construct the board
	def init_board(self):

		'''
		Possible board values:
		'w' : Wall
		'e' : Empty
		'c' : Cherry
		'h' : Snake head
		'u' : Snake body, direction up
		'd' : Snake body, direction down
		'l' : Snake body, direction left
		'r' : Snake body, direction right
		'''

		self.board = np.empty((self.board_height, self.board_width), dtype='object') 
		
		'''
		THERE HAS TO BE A MORE SPECIFIC DTYPE FOR TKINTER BUTTONS
		INIT AND PACK ALL BUTTONS INTO GRID
		'''
		
		# Init all values to zero
		for i in range(self.board_height):
			for j in range(self.board_width):
				self.board[i, j].value = 'e'

		# Build the wall
		for i in range(self.board_height):
			self.board[i,                    0].value = 'w'
			self.board[i, self.board_width - 1].value = 'w'

		for j in range(self.board_width):
			self.board[                    0, j].value = 'w'
			self.board[self.board_height - 1, j].value = 'w'

	# Construct the snake
	def init_snake(self):
		
		# Randomly generate snake head
		self.head_i = randint(self.snake_init_length, self.board_height - self.snake_init_length - 1)
		self.head_i = randint(self.snake_init_length, self.board_width  - self.snake_init_length - 1)
		self.board[self.head_i, self.head_j] = 'h'
		
		# Build tail in random direction
		direction = randint(0, 3)
		for k in range(1, snake_init_length):

			# Head pointing up
			if direction == 0:
				self.tail_i = self.head_i + k
				self.tail_j = self.head_j
				self.board[self.tail_i, self.tail_j].value = 'u'
			
			# Head pointing down
			elif direction == 1:
				self.tail_i = self.head_i - k
				self.tail_j = self.head_j
				self.board[self.tail_i, self.tail_j].value = 'd'
			
			# Head pointing left
			elif direction == 2:
				self.tail_i = self.head_i
				self.tail_j = self.head_j + k
				self.board[self.tail_i, self.tail_j].value = 'l'
			
			# Head pointing right
			elif direction == 3:
				self.tail_i = self.head_i
				self.tail_j = self.head_j - k
				self.board[self.tail_i, self.tail_j].value = 'r'
	
	# Spawn the cherry
	def init_cherry(self):

		while True:

			# Spawn at random location not within snake
			i = randint(1, board_height - 2)
			j = randint(1, board_height - 2)

			if self.board[i, j].value == 'e':
				self.board[i, j].value = 'c'
				break
	
	# Displace the snake by one tick
	def move_snake(self, head_dir):
		
		# Grow tail
		if self.tail_delay != 0:
			self.tail_delay -= 1

		# Receeding tail
		else:
			tail_dir = self.board[self.tail_i, self.tail_j].value
			self.board[self.tail_i, self.tail_j].value = 'e'

			if tail_dir == 'u':
				self.tail_i -= 1
			elif tail_dir == 'd':
				self.tail_i += 1
			elif tail_dir == 'l':
				self.tail_j -= 1
			elif tail_dir == 'r':
				self.tail_j += 1

		# Advance the head
		self.board[self.head_i, self.head_j] = head_dir

		if head_dir == 'u':
			self.head_i -= 1
		elif head_dir == 'd':
			self.head_i += 1
		elif head_dir == 'l':
			self.head_j -= 1
		elif head_dir == 'r':
			self.head_j += 1

		# Check for head colliison
		if self.board[self.head_i, self.head_j] == 'c':

			# Captured cherry
			self.board[self.head_i, self.head_j] = 'h'
			self.tail_delay += self.snake_apple_growth
			self.score += 1
			self.init_cherry()

		elif self.board[self.head_i, self.head_j] != 'e':

			# Brutal collision
			print('Ouch')
			self.game_state = 0

		else:

			# Free real estate
			self.board[self.head_i, self.head_j] = 'h'
