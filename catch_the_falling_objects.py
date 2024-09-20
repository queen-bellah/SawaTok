import tkinter as tk
import random
import pygame
from PIL import Image, ImageTk  # Import PIL for resizing images

# Initialize the main window
root = tk.Tk()
root.title("Catch the Falling Objects - Fun for Kids!")
root.resizable(False, False)

# Initialize Pygame mixer for sound effects
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 600, 400
BASKET_WIDTH, BASKET_HEIGHT = 80, 40  # Adjusted basket size for better aspect ratio
OBJECT_SIZE = 30  # Reduced size for falling objects
BASKET_SPEED = 15  # Increased speed for basket movement
FALL_SPEED = 7
CATCH_POINTS = 10

# Canvas to draw the game
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
canvas.pack()

# Load and resize basket image while maintaining aspect ratio
basket_image = Image.open("bas.png")  # Load the basket image
basket_image.thumbnail((BASKET_WIDTH, BASKET_HEIGHT), Image.ANTIALIAS)  # Resize while maintaining aspect ratio
basket_img = ImageTk.PhotoImage(basket_image)  # Convert to Tkinter format
basket = canvas.create_image(WIDTH // 2, HEIGHT - 40, image=basket_img)

# Initialize score
score = 0
score_label = tk.Label(root, text=f"Score: {score}", font=("Comic Sans MS", 16), bg="yellow")
score_label.pack()

# Load and resize falling object images (like fruits)
object_images = []
for fruit_file in ["apple.png", "apple.png", "apple.png", "apple.png"]:
    img = Image.open(fruit_file)
    img = img.resize((OBJECT_SIZE, OBJECT_SIZE), Image.ANTIALIAS)  # Resize to 30x30 pixels
    object_images.append(ImageTk.PhotoImage(img))

# Variables to track basket movement
basket_x_velocity = 0

# Create falling objects list
falling_objects = []

# Function to move basket
def move_basket():
    global basket_x_velocity
    canvas.move(basket, basket_x_velocity, 0)
    basket_pos = canvas.coords(basket)

    # Prevent the basket from going out of bounds
    if basket_pos[0] < 40:  # Adjust for image width
        canvas.coords(basket, 40, basket_pos[1])
    if basket_pos[0] > WIDTH - 40:
        canvas.coords(basket, WIDTH - 40, basket_pos[1])

# Function to create random falling objects
def spawn_falling_object():
    x = random.randint(40, WIDTH - 40)
    y = 0
    img = random.choice(object_images)
    falling_object = canvas.create_image(x, y, image=img)
    falling_objects.append(falling_object)

# Function to move falling objects
def move_falling_objects():
    global score
    for falling_object in falling_objects:
        canvas.move(falling_object, 0, FALL_SPEED)
        object_pos = canvas.coords(falling_object)

        # If the object reaches the bottom, remove it
        if object_pos[1] >= HEIGHT:
            canvas.delete(falling_object)
            falling_objects.remove(falling_object)
        # Check if the object is caught by the basket
        elif check_catch(object_pos):
            # pygame.mixer.Sound.play(catch_sound)  # Play sound effect when caught
            canvas.delete(falling_object)
            falling_objects.remove(falling_object)
            score += CATCH_POINTS
            score_label.config(text=f"Score: {score}")

# Function to check if the basket catches the falling object
def check_catch(object_pos):
    basket_pos = canvas.coords(basket)
    if abs(basket_pos[0] - object_pos[0]) < 40 and object_pos[1] >= HEIGHT - 60:
        return True
    return False

# Function to handle key presses (move basket)
def key_press(event):
    global basket_x_velocity
    if event.keysym == "Left":
        basket_x_velocity = -BASKET_SPEED
    elif event.keysym == "Right":
        basket_x_velocity = BASKET_SPEED

# Function to handle key releases (stop basket)
def key_release(event):
    global basket_x_velocity
    if event.keysym in ["Left", "Right"]:
        basket_x_velocity = 0

# Function to update the game state
def update_game():
    move_basket()
    move_falling_objects()

    # Spawn new falling objects randomly
    if random.randint(1, 100) > 95:
        spawn_falling_object()

    # Call update_game again after 50 milliseconds
    root.after(50, update_game)

# Bind arrow keys to basket movement
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# Start the game
update_game()

# Run the Tkinter event loop
root.mainloop()
