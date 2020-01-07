'''
Package importing
'''
import numpy as np
import tkinter as tk
import random as rand

'''
Tkinter management (GUI stuff)
'''
root = tk.Tk()
root.title("Snake Game")
board_frame = tk.Frame(root)
board_frame.pack()


'''
Score display
'''
lower_frame = tk.Frame(root)
lower_frame.pack()
score_label = tk.Label(lower_frame, relief='groove')
score_label.pack()

def set_score():
    global score
    score_label.config(text = 'Score = %d' % score)
    return

'''
Move display
'''
move_label = tk.Label(lower_frame, relief='groove')
move_label.pack()

def set_move():
    global move
    move_label.config(text = 'Move: %d' % move)
    return

'''
Fitness display
'''
fitness_label = tk.Label(lower_frame, relief='groove')
fitness_label.pack()

def set_fitness():
    global fitness
    fitness_label.config(text = 'Fitness: %.2f' % fitness)
    return

'''
Game number display
'''
game_number_label = tk.Label(lower_frame, relief='groove')
game_number_label.pack()

def set_game_number():
    global games_played
    game_number_label.config(text = 'Game number: %d' % (games_played + 1))
    return


'''
Initialization functions
'''
def initial_board_generation():
    global board_size
    
    board_array = np.empty((board_size, board_size), dtype = 'object')
    for i in range(board_size):
        for j in range(board_size):
            if i == 0 or i == board_size-1 or j == 0 or j == board_size-1:
                color = 'black'
            else:
                color = 'grey'
            board_array[i,j] = tk.Label(board_frame, bg=color, height=1, width=2, relief='sunken')
            board_array[i,j].grid(row=i, column=j)
    return board_array

def initial_snake_generation(snake_len = 4):
    global board_array, board_size
    
    snake_array = np.empty((snake_len, 2), dtype = 'int')
    j = rand.randint(2, 5)
    k = rand.randint(snake_len+1, board_size-10)
    for x in range(snake_len):
        i = k - x
        board_array[i,j].config(bg='white', relief='groove')
        snake_array[x,:] = i, j
    return snake_array

def initial_cherry_generation():
    global board_array, board_size
    
    i = rand.randint(1, board_size-2)
    j = rand.randint(6, board_size-2)
    board_array[i,j].config(bg='red', relief='groove')
    cherry_array = np.array([i, j])
    return cherry_array

def initial_variables():
    score = 0
    snake_babies = 0
    current_direction = -1
    last_direction = -1
    fitness = 0
    move = 0
    return score, snake_babies, current_direction, last_direction, fitness, move


'''
Let's make something clear about the movement:
    If I am moving up, my direction value is 1
    If I am moving down, my direction value is -1
    .............. right, ........... value is 2
    .............. left, ............ value is -2
    Therefore, the snake cannot move a direction IFF 
        current_direction + last_direction == 0
    (you cannot instantly take a 180 degree turn)
    If that is the case, set current_direction = last_direction
'''

'''
Movement function
'''
def snake_advance():
    global board_size, board_array, snake_array, cherry_array, score
    global snake_babies, current_direction, last_direction, game_state
    global fitness, move
    
    # Make sure game is active
    if not game_state:
        return
    
    # Schedule next snake advance function call
    root.after(40, snake_advance)
    
    # Increment move counter
    move += 1
    set_move()
    
    # Locate old snake head position
    old_i, old_j = snake_array[0,:]
    
    # Ensure not moving opposite last direction moved
    if current_direction + last_direction == 0:
        current_direction = last_direction
    
    # Determine new head position
    if current_direction == 1:
        new_i = old_i - 1
        new_j = old_j
    elif current_direction == -1:
        new_i = old_i + 1
        new_j = old_j
    elif current_direction == -2:
        new_i = old_i
        new_j = old_j - 1
    elif current_direction == 2:
        new_i = old_i
        new_j = old_j + 1
    
    # Store last move
    last_direction = current_direction
    
    # Determine what square the head is about to step on
    color_stepped = board_array[new_i, new_j]["bg"]
    
    # Add head on board and append to snake array
    head = np.array([new_i, new_j])
    board_array[new_i, new_j].config(bg='white', relief='groove')
    snake_array = np.vstack((head, snake_array))
    
    # If consumes cherry
    if color_stepped == "red":
        score += 1
        snake_babies += 5
        set_score()
        
        # Generate new cherry, NOT where snake is currently
        while True:
            i = rand.randint(1, board_size-2)
            j = rand.randint(1, board_size-2)
            if board_array[i,j]["bg"] == 'grey':
                break
        
        cherry_array = np.array([i,j])
        board_array[i,j].config(bg='red', relief='groove')
    
    # If walks out of bounds
    elif color_stepped == "black":
        board_array[new_i, new_j].config(bg='yellow', relief='groove')
        game_over()
        return
        
    # If self-colision
    elif color_stepped == "white":
        board_array[new_i, new_j].config(bg='yellow', relief='groove')
        game_over()
        return
        
    # Check if tail needs to be deleted or if staying due to cherry consumption
    if snake_babies:
        snake_babies -= 1
    else:
        dead_i, dead_j = snake_array[-1,:]
        board_array[dead_i, dead_j].config(bg='grey', relief='sunken')
        snake_array = snake_array[:-1,:]
    
    return


'''
End of session
'''
def game_over():
    global game_state, move, score, fitness
    game_state = 0
    
    # Determine fitness
    if score < 5:
        fitness = score + 1 / (1 + np.exp(-1*move))
    elif score > 20:
        fitness = score - 1 / (1 + np.exp(-1*move))
    else:
        fitness = score

    # IT SEEMS TO ONLY BE OUTPUTTING INTEGER FITNESS VALS
    
    set_fitness()
    return

'''
Manual keyboard control system
'''
def leftKey(event):
    global current_direction
    current_direction = -2
    return

def rightKey(event):
    global current_direction
    current_direction = 2
    return

def upKey(event):
    global current_direction
    current_direction = 1
    return

def downKey(event):
    global current_direction
    current_direction = -1
    return
    
board_frame.bind('<Left>', leftKey)
board_frame.bind('<Right>', rightKey)
board_frame.bind('<Up>', upKey)
board_frame.bind('<Down>', downKey)
board_frame.focus_set()


'''
Game start/reset system
'''
def start():
    global board_size, board_array, snake_array, cherry_array, score
    global snake_babies, current_direction, last_direction, game_state
    global games_played, fitness, move
    
    # Don't restart if game in progress (makes game double speed idk)
    if game_state:
        return
    
    game_state = 1
    
    if games_played:
        
        # Remove cherry
        cherry_i, cherry_j = cherry_array
        board_array[cherry_i, cherry_j].config(bg='grey', relief='sunken')
        
        # Restore snake_array to grey squares
        for x in range(snake_array.shape[0]):
            snake_i, snake_j = snake_array[x,:]
            board_array[snake_i, snake_j].config(bg='grey', relief='sunken')
        
        # Change head back to appropriate colour
        head_i, head_j = snake_array[0,:]
        if head_i == 0 or head_i == board_size-1 or head_j == 0 or head_j == board_size-1:
            board_array[head_i, head_j].config(bg='black', relief='sunken')
        
        snake_array = initial_snake_generation()
        cherry_array = initial_cherry_generation()
        score, snake_babies, current_direction, last_direction, fitness, move = initial_variables()
    
    set_game_number()
    games_played += 1
    set_score()
    set_move()
    set_fitness()
    snake_advance()
    return

start_button = tk.Button(lower_frame, text="Start Game", relief='groove', command=start,
                         bg='black', fg='white')
start_button.pack()


'''
Initializing global variables to run it all
'''
games_played = 0
game_state = 0
board_size = 25
board_array = initial_board_generation()
snake_array = initial_snake_generation()
cherry_array = initial_cherry_generation()
score, snake_babies, current_direction, last_direction, fitness, move = initial_variables()
set_score()
set_move()
set_fitness()
set_game_number()

root.mainloop()

# ADD HIGH SCORE