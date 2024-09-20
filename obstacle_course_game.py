import tkinter as tk
import random

# Initialize the main window
root = tk.Tk()
root.title("Obstacle Course Game")
root.resizable(False, False)

# Constants
WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 50
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 30, 70
GROUND = HEIGHT - PLAYER_SIZE
GRAVITY = 2
JUMP_STRENGTH = -20
SPEED = 5

# Canvas to draw the game
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
canvas.pack()

# Create the ground
canvas.create_rectangle(0, GROUND, WIDTH, HEIGHT, fill="green")

# Player (rectangle for simplicity)
player = canvas.create_rectangle(50, GROUND - PLAYER_SIZE, 50 + PLAYER_SIZE, GROUND, fill="blue")

# Obstacle
obstacles = []

# Variables to track player movement
y_velocity = 0
is_jumping = False

# Function to make the player jump
def jump(event):
    global y_velocity, is_jumping
    if not is_jumping:  # Prevent double jumps
        y_velocity = JUMP_STRENGTH
        is_jumping = True

# Function to update the game state
def update_game():
    global y_velocity, is_jumping, obstacles, SPEED
    
    # Gravity effect on player
    canvas.move(player, 0, y_velocity)
    player_pos = canvas.coords(player)
    
    if player_pos[3] >= GROUND:  # If player is on the ground
        canvas.coords(player, player_pos[0], GROUND - PLAYER_SIZE, player_pos[2], GROUND)
        y_velocity = 0
        is_jumping = False
    else:
        y_velocity += GRAVITY
    
    # Move obstacles
    for obstacle in obstacles:
        canvas.move(obstacle, -SPEED, 0)
        obstacle_pos = canvas.coords(obstacle)
        if obstacle_pos[2] < 0:  # Remove obstacle if it goes off screen
            canvas.delete(obstacle)
            obstacles.remove(obstacle)
        
        # Check for collision with the player
        if check_collision(player_pos, obstacle_pos):
            game_over()
            return
    
    # Spawn new obstacles randomly
    if random.randint(1, 100) > 98:
        spawn_obstacle()

    # Increase speed to make the game harder
    SPEED += 0.001
    
    # Call update_game again after 50 milliseconds
    root.after(50, update_game)

# Function to spawn obstacles
def spawn_obstacle():
    y1 = GROUND - OBSTACLE_HEIGHT
    y2 = GROUND
    x1 = WIDTH
    x2 = WIDTH + OBSTACLE_WIDTH
    obstacle = canvas.create_rectangle(x1, y1, x2, y2, fill="red")
    obstacles.append(obstacle)

# Function to check for collision between player and obstacle
def check_collision(player_pos, obstacle_pos):
    if (player_pos[2] > obstacle_pos[0] and player_pos[0] < obstacle_pos[2] and
        player_pos[3] > obstacle_pos[1] and player_pos[1] < obstacle_pos[3]):
        return True
    return False

# Function to handle game over
def game_over():
    canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", font=("Arial", 30), fill="white")
    root.after(2000, root.quit)  # Close game after 2 seconds

# Bind the space key to jump
root.bind("<space>", jump)

# Start the game
update_game()

# Run the Tkinter event loop
root.mainloop()
