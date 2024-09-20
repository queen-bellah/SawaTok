import tkinter as tk
import random
import pygame

# Initialize the main window
root = tk.Tk()
root.title("Animal Chase Game")
root.resizable(False, False)

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Load the sound file
catch_sound = pygame.mixer.Sound("catch.wav")  # Make sure to have a sound file named 'catch.wav' in your directory

# Constants
WIDTH, HEIGHT = 600, 400
PLAYER_SIZE = 50
TARGET_SIZE = 30
SPEED = 10
TIME_LIMIT = 30  # Time limit in seconds

# Canvas to draw the game
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
canvas.pack()

# Create the player (Dog or Cat)
player = canvas.create_rectangle(50, HEIGHT // 2 - PLAYER_SIZE // 2, 50 + PLAYER_SIZE, HEIGHT // 2 + PLAYER_SIZE // 2, fill="brown")

# Create multiple targets (objects to catch)
targets = [canvas.create_oval(WIDTH - TARGET_SIZE, random.randint(0, HEIGHT - TARGET_SIZE),
                             WIDTH, random.randint(0, HEIGHT - TARGET_SIZE) + TARGET_SIZE, fill="red") for _ in range(3)]

# Power-up
power_up = None

# Variables to track player movement
player_x_velocity = 0
player_y_velocity = 0
time_remaining = TIME_LIMIT
speed_boost = 1  # Multiplier for speed (increases with power-up)

# Function to move player
def move_player():
    global player_x_velocity, player_y_velocity

    canvas.move(player, player_x_velocity * speed_boost, player_y_velocity * speed_boost)
    player_pos = canvas.coords(player)

    # Prevent the player from going out of bounds
    if player_pos[0] < 0:
        canvas.coords(player, 0, player_pos[1], PLAYER_SIZE, player_pos[3])
    if player_pos[2] > WIDTH:
        canvas.coords(player, WIDTH - PLAYER_SIZE, player_pos[1], WIDTH, player_pos[3])
    if player_pos[1] < 0:
        canvas.coords(player, player_pos[0], 0, player_pos[2], PLAYER_SIZE)
    if player_pos[3] > HEIGHT:
        canvas.coords(player, player_pos[0], HEIGHT - PLAYER_SIZE, player_pos[2], HEIGHT)

# Function to check if the player caught a target
def check_collision():
    player_pos = canvas.coords(player)
    for target in targets:
        target_pos = canvas.coords(target)
        if (player_pos[2] > target_pos[0] and player_pos[0] < target_pos[2] and
            player_pos[3] > target_pos[1] and player_pos[1] < target_pos[3]):
            return target
    return None

# Function to move the targets randomly
def move_targets():
    for target in targets:
        canvas.move(target, random.randint(-SPEED, SPEED), random.randint(-SPEED, SPEED))
        target_pos = canvas.coords(target)

        # Prevent the target from going out of bounds
        if target_pos[0] < 0 or target_pos[2] > WIDTH:
            canvas.move(target, -SPEED, 0)
        if target_pos[1] < 0 or target_pos[3] > HEIGHT:
            canvas.move(target, 0, -SPEED)

# Function to handle key presses (move player)
def key_press(event):
    global player_x_velocity, player_y_velocity

    if event.keysym == "Up":
        player_y_velocity = -SPEED
    elif event.keysym == "Down":
        player_y_velocity = SPEED
    elif event.keysym == "Left":
        player_x_velocity = -SPEED
    elif event.keysym == "Right":
        player_x_velocity = SPEED

# Function to handle key releases (stop player)
def key_release(event):
    global player_x_velocity, player_y_velocity

    if event.keysym in ["Up", "Down"]:
        player_y_velocity = 0
    if event.keysym in ["Left", "Right"]:
        player_x_velocity = 0

# Function to update the game state
def update_game():
    global time_remaining

    # Move the player and targets
    move_player()
    move_targets()

    # Check for collisions
    target_hit = check_collision()
    if target_hit:
        pygame.mixer.Sound.play(catch_sound)  # Play the catch sound when target is hit
        canvas.delete(target_hit)
        targets.remove(target_hit)
        
        if len(targets) == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="You Win!", font=("Arial", 30), fill="green")
            root.after(2000, root.quit)
            return

    # Update time remaining
    time_remaining -= 1
    if time_remaining <= 0:
        canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Time's Up!", font=("Arial", 30), fill="red")
        root.after(2000, root.quit)
        return

    # Call update_game again after 100 milliseconds
    root.after(100, update_game)

# Bind arrow keys to player movement
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# Start the game
update_game()

# Run the Tkinter event loop
root.mainloop()
