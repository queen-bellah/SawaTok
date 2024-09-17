import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3

# Initialize the main window
root = tk.Tk()
root.title("Speech Practice Interface")
root.attributes("-fullscreen", True)

# Initialize pyttsx3 for Text-to-Speech
tts_engine = pyttsx3.init()

# Set the voice to English (America)
voices = tts_engine.getProperty('voices')
tts_engine.setProperty('voice', voices[24].id)  # Selecting "English (America)"

# Adjust speed and volume
tts_engine.setProperty('rate', 150)  # Adjust for slower speech if needed
tts_engine.setProperty('volume', 1.0)  # Set to maximum volume

# List of image paths and their corresponding texts
images_data = [
    {"image_path": "all.jpg", "text": "Say this is a dog"},
    {"image_path": "cat.jpg", "text": "Say this is a cat"},
    {"image_path": "bed.jpg", "text": "Say this is a bed"}
]

# Variable to keep track of the current image index
current_index = 0

# Function to use pyttsx3 to speak the text
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to update the displayed image and text
def update_image():
    global current_index
    image_path = images_data[current_index]["image_path"]
    instruction_text = images_data[current_index]["text"]
    
    # Load and display the image
    image = Image.open(image_path)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    image = image.resize((screen_width, screen_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection

    text_label.config(text=instruction_text)
    text_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

    # Delay the speech to ensure the image is displayed first
    root.after(500, lambda: speak_text(instruction_text))

# Function to go to the next image
def next_image():
    global current_index
    if current_index < len(images_data) - 1:
        current_index += 1
    else:
        current_index = 0  # Loop back to the first image
    update_image()

# Function to go to the previous image
def previous_image():
    global current_index
    if current_index > 0:
        current_index -= 1
    else:
        current_index = len(images_data) - 1  # Loop back to the last image
    update_image()

# Create a label to display the image
image_label = tk.Label(root)
image_label.pack(fill=tk.BOTH, expand=True)

# Create a label for the instruction text (overlay on image)
text_label = tk.Label(root, text="", font=("Arial", 20), bg="white", fg="black")

# Create Previous and Next buttons
prev_button = tk.Button(root, text="Previous", font=("Arial", 14), bg="blue", fg="white", width=10, command=previous_image)
prev_button.place(relx=0.05, rely=0.9)  # Positioned at the left bottom corner

next_button = tk.Button(root, text="Next", font=("Arial", 14), bg="green", fg="white", width=10, command=next_image)
next_button.place(relx=0.85, rely=0.9)  # Positioned at the right bottom corner

# Initialize by showing the first image
update_image()

# Run the Tkinter event loop
root.mainloop()


