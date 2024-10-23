# import tkinter as tk
# from PIL import Image, ImageTk
# from TTS.api import TTS
# import threading
# import random
# import time

# # Initialize the main window
# root = tk.Tk()
# root.title("Game Level Selection")
# root.geometry("800x600")  # Set the window size
# root.configure(bg="white")

# # Initialize Coqui TTS
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_path="vocoder_models/en/ljspeech/hifigan_v2")

# # Lock to prevent speech overlap
# voice_lock = threading.Lock()

# # List of image paths and their corresponding texts (20 images)
# images_data = [
#     {"image_path": "all.jpg", "text": "This is a ball"},
#     {"image_path": "cat.jpg", "text": "This is a cat"},
#     {"image_path": "bed.jpg", "text": "This is a bed"},
#     {"image_path": "donkey.jpeg", "text": "This is a donkey"},
#     {"image_path": "owl.jpg", "text": "This is an owl"},
#     {"image_path": "bus(1).jpg", "text": "This is a bus"},
#     {"image_path": "bowl.jpg", "text": "This is a banana"},
#     {"image_path": "bell.jpg", "text": "This is a bell"},
#     {"image_path": "ball.jpg", "text": "This is a ball"},
#     {"image_path": "crocodile.jpg", "text": "This is a crocodile"},
#     {"image_path": "whiteduck.jpg", "text": "This is a white duck"},
#     {"image_path": "turtle.jpg", "text": "This is a turtle"},
#     {"image_path": "butterfly.jpg", "text": "This is a butterfly"},
#     {"image_path": "books.jpg", "text": "These are books"},
#     {"image_path": "duck.jpg", "text": "This is a duck"},
#     {"image_path": "bat.jpg", "text": "This is a bat"},
#     {"image_path": "monkey.jpg", "text": "This is a monkey"},
#     {"image_path": "zebra.jpg", "text": "This is a zebra"},
#     {"image_path": "fox.jpg", "text": "This is a fox"},
#     {"image_path": "boat.jpg", "text": "This is a boat"}
# ]

# # Variable to keep track of the current image index
# current_index = 0

# # Function to use Coqui TTS to speak the text
# def speak_text(text):
#     with voice_lock:
#         print(f"Speaking: {text}")
#         tts.tts_to_file(text=text, file_path="tts_output.wav")
#         play_audio("tts_output.wav")

# # Function to play audio using simpleaudio
# def play_audio(filename):
#     import simpleaudio as sa
#     wave_obj = sa.WaveObject.from_wave_file(filename)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()

# # Function to resize the image while maintaining aspect ratio
# def resize_image(image, max_width, max_height):
#     img_width, img_height = image.size
#     ratio = min(max_width / img_width, max_height / img_height)
#     new_width = int(img_width * ratio)
#     new_height = int(img_height * ratio)
#     return image.resize((new_width, new_height), Image.ANTIALIAS)

# # Function to update the displayed image and text
# def update_image():
#     global current_index
#     image_path = images_data[current_index]["image_path"]
#     instruction_text = images_data[current_index]["text"]
    
#     # Load and display the image
#     image = Image.open(image_path)
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
    
#     # Resize the image to fit the screen while maintaining the aspect ratio
#     image = resize_image(image, screen_width, screen_height)
#     photo = ImageTk.PhotoImage(image)
#     image_label.config(image=photo)
#     image_label.image = photo  # Keep a reference to avoid garbage collection

#     text_label.config(text=instruction_text)
#     text_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

#     # Delay the speech to ensure the image is displayed first
#     root.after(500, lambda: threading.Thread(target=speak_text, args=(instruction_text,)).start())

# # Function to go to the next image
# def next_image():
#     global current_index
#     if current_index < len(images_data) - 1:
#         current_index += 1
#     else:
#         current_index = 0  # Loop back to the first image
#     update_image()

# # Function to go to the previous image
# def previous_image():
#     global current_index
#     if current_index > 0:
#         current_index -= 1
#     else:
#         current_index = len(images_data) - 1  # Loop back to the last image
#     update_image()

# # Function to switch from game level screen to main image display
# def show_main_screen():
#     for widget in root.winfo_children():
#         widget.destroy()  # Clear the current screen

#     # Create a label to display the image
#     global image_label
#     image_label = tk.Label(root)
#     image_label.pack(fill=tk.BOTH, expand=True)

#     # Create a label for the instruction text (overlay on image)
#     global text_label
#     text_label = tk.Label(root, text="", font=("Arial", 20), bg="white", fg="black")

#     # Create Previous and Next buttons
#     prev_button = tk.Button(root, text="Previous", font=("Arial", 14), bg="blue", fg="white", width=10, command=previous_image)
#     prev_button.place(relx=0.05, rely=0.9)  # Positioned at the left bottom corner

#     next_button = tk.Button(root, text="Next", font=("Arial", 14), bg="green", fg="white", width=10, command=next_image)
#     next_button.place(relx=0.85, rely=0.9)  # Positioned at the right bottom corner

#     # Initialize by showing the first image
#     update_image()

# # Function to create the game level selection screen
# def game_levels_screen():
#     # Title label
#     title_label = tk.Label(root, text="Game Levels", font=("Arial", 30), bg="white")
#     title_label.pack(pady=20)

#     # Create a frame for the game levels
#     level_frame = tk.Frame(root, bg="white")
#     level_frame.pack(pady=20)

#     # Image and button for Easy level
#     easy_img = Image.open("smileydog.jpg")  # Replace with your image path
#     easy_img = easy_img.resize((150, 150), Image.ANTIALIAS)
#     easy_photo = ImageTk.PhotoImage(easy_img)

#     easy_label = tk.Label(level_frame, image=easy_photo, bg="white")
#     easy_label.image = easy_photo
#     easy_label.grid(row=0, column=0, padx=30)

#     easy_button = tk.Button(level_frame, text="Start", command=show_main_screen, bg="green", fg="white", font=("Arial", 12))
#     easy_button.grid(row=1, column=0)

#     easy_text = tk.Label(level_frame, text="Easy", font=("Arial", 14), bg="white")
#     easy_text.grid(row=2, column=0, pady=10)

#     # Image and button for Medium level (Locked)
#     medium_img = Image.open("boy1.png")  # Replace with your image path
#     medium_img = medium_img.resize((150, 150), Image.ANTIALIAS)
#     medium_photo = ImageTk.PhotoImage(medium_img)

#     medium_label = tk.Label(level_frame, image=medium_photo, bg="white")
#     medium_label.image = medium_photo
#     medium_label.grid(row=0, column=1, padx=30)

#     medium_button = tk.Button(level_frame, text="Locked", state="disabled", bg="gray", fg="white", font=("Arial", 12))
#     medium_button.grid(row=1, column=1)

#     medium_text = tk.Label(level_frame, text="Medium", font=("Arial", 14), bg="white")
#     medium_text.grid(row=2, column=1, pady=10)

#     # Image and button for Hard level (Locked)
#     hard_img = Image.open("boy1.png")  # Replace with your image path
#     hard_img = hard_img.resize((150, 150), Image.ANTIALIAS)
#     hard_photo = ImageTk.PhotoImage(hard_img)

#     hard_label = tk.Label(level_frame, image=hard_photo, bg="white")
#     hard_label.image = hard_photo
#     hard_label.grid(row=0, column=2, padx=30)

#     hard_button = tk.Button(level_frame, text="Locked", state="disabled", bg="gray", fg="white", font=("Arial", 12))
#     hard_button.grid(row=1, column=2)

#     hard_text = tk.Label(level_frame, text="Hard", font=("Arial", 14), bg="white")
#     hard_text.grid(row=2, column=2, pady=10)

# # Create a loading screen with a background image and progress bar
# def loading_screen():
#     # Load and display the background image for the loading screen
#     bg_image = Image.open("boy.jpg")  # Replace with your background image path
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     bg_image = bg_image.resize((screen_width, screen_height), Image.ANTIALIAS)
#     bg_photo = ImageTk.PhotoImage(bg_image)
    
#     bg_label = tk.Label(root, image=bg_photo)
#     bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
#     bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Set the image to cover the full screen

#     load_label = tk.Label(root, text="Unlock Your Full Potential", font=("Arial", 40), fg="green", bg="lightblue")
#     load_label.pack(pady=200)

#     # Create the progress bar
#     progress_bar = tk.Canvas(root, width=400, height=30, bg="white", highlightthickness=0)
#     progress_bar.pack(pady=20)
#     load_progress = progress_bar.create_rectangle(0, 0, 0, 30, fill="green")

#     def fill_bar():
#         for i in range(1, 101):
#             progress_bar.coords(load_progress, (0, 0, i * 4, 30))
#             root.update_idletasks()
#             time.sleep(0.1)  # Simulate loading time

#         # Remove loading screen elements
#         load_label.destroy()
#         progress_bar.destroy()
#         bg_label.destroy()

#         # Show the level selection screen
#         game_levels_screen()

#     threading.Thread(target=fill_bar).start()

# # Start with the loading screen
# loading_screen()

# # Run the Tkinter event loop
# root.mainloop()


# import tkinter as tk
# # from PIL import Image, ImageTk
# from PIL import Image, ImageTk
# from TTS.api import TTS
# import threading
# import random
# import time
# import simpleaudio as sa

# # Initialize the main window
# root = tk.Tk()
# root.title("Game Level Selection")
# root.geometry("800x600")  # Set the window size
# root.configure(bg="white")

# # Initialize Coqui TTS
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_path="vocoder_models/en/ljspeech/hifigan_v2")

# # Lock to prevent speech overlap
# voice_lock = threading.Lock()

# # List of image paths and their corresponding texts (20 images)
# images_data = [
#     {"image_path": "all.jpg", "text": "This is a ball"},
#     {"image_path": "cat.jpg", "text": "This is a cat"},
#     {"image_path": "bed.jpg", "text": "This is a bed"},
#     {"image_path": "donkey.jpeg", "text": "This is a donkey"},
#     {"image_path": "owl.jpg", "text": "This is an owl"},
#     {"image_path": "bus(1).jpg", "text": "This is a bus"},
#     {"image_path": "bowl.jpg", "text": "This is a banana"},
#     {"image_path": "bell.jpg", "text": "This is a bell"},
#     {"image_path": "ball.jpg", "text": "This is a ball"},
#     {"image_path": "crocodile.jpg", "text": "This is a crocodile"},
#     {"image_path": "whiteduck.jpg", "text": "This is a white duck"},
#     {"image_path": "turtle.jpg", "text": "This is a turtle"},
#     {"image_path": "butterfly.jpg", "text": "This is a butterfly"},
#     {"image_path": "books.jpg", "text": "These are books"},
#     {"image_path": "duck.jpg", "text": "This is a duck"},
#     {"image_path": "bat.jpg", "text": "This is a bat"},
#     {"image_path": "monkey.jpg", "text": "This is a monkey"},
#     {"image_path": "zebra.jpg", "text": "This is a zebra"},
#     {"image_path": "fox.jpg", "text": "This is a fox"},
#     {"image_path": "boat.jpg", "text": "This is a boat"}
# ]

# # Variable to keep track of the current image index
# current_index = 0

# # Function to use Coqui TTS to speak the text
# def speak_text(text):
#     with voice_lock:
#         print(f"Speaking: {text}")
#         tts.tts_to_file(text=text, file_path="tts_output.wav")
#         play_audio("tts_output.wav")

# # Function to play audio using simpleaudio
# def play_audio(filename):
#     wave_obj = sa.WaveObject.from_wave_file(filename)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()

# # Function to resize the image while maintaining aspect ratio
# def resize_image(image, max_width, max_height):
#     img_width, img_height = image.size
#     ratio = min(max_width / img_width, max_height / img_height)
#     new_width = int(img_width * ratio)
#     new_height = int(img_height * ratio)
#     return image.resize((new_width, new_height), Image.LANCZOS)

# # Function to update the displayed image and text
# def update_image():
#     global current_index
#     image_path = images_data[current_index]["image_path"]
#     instruction_text = images_data[current_index]["text"]
    
#     # Load and display the image
#     image = Image.open(image_path)
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
    
#     # Resize the image to fit the screen while maintaining the aspect ratio
#     image = resize_image(image, screen_width, screen_height)
#     photo = ImageTk.PhotoImage(image)
#     image_label.config(image=photo)
#     image_label.image = photo  # Keep a reference to avoid garbage collection

#     text_label.config(text=instruction_text)
#     text_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

#     # Delay the speech to ensure the image is displayed first
#     root.after(500, lambda: threading.Thread(target=speak_text, args=(instruction_text,)).start())

# # Function to go to the next image
# def next_image():
#     global current_index
#     if current_index < len(images_data) - 1:
#         current_index += 1
#     else:
#         current_index = 0  # Loop back to the first image
#     update_image()

# # Function to go to the previous image
# def previous_image():
#     global current_index
#     if current_index > 0:
#         current_index -= 1
#     else:
#         current_index = len(images_data) - 1  # Loop back to the last image
#     update_image()

# # Function to switch from game level screen to main image display
# def show_main_screen():
#     for widget in root.winfo_children():
#         widget.destroy()  # Clear the current screen

#     # Create a label to display the image
#     global image_label
#     image_label = tk.Label(root)
#     image_label.pack(fill=tk.BOTH, expand=True)

#     # Create a label for the instruction text (overlay on image)
#     global text_label
#     text_label = tk.Label(root, text="", font=("Arial", 20), bg="white", fg="black")

#     # Create Previous and Next buttons
#     prev_button = tk.Button(root, text="Previous", font=("Arial", 14), bg="blue", fg="white", width=10, command=previous_image)
#     prev_button.place(relx=0.05, rely=0.9)  # Positioned at the left bottom corner

#     next_button = tk.Button(root, text="Next", font=("Arial", 14), bg="green", fg="white", width=10, command=next_image)
#     next_button.place(relx=0.85, rely=0.9)  # Positioned at the right bottom corner

#     # Initialize by showing the first image
#     update_image()

# # Function to create the game level selection screen
# def game_levels_screen():
#     # Title label
#     title_label = tk.Label(root, text="Game Levels", font=("Arial", 30), bg="white")
#     title_label.pack(pady=20)

#     # Create a frame for the game levels
#     level_frame = tk.Frame(root, bg="white")
#     level_frame.pack(pady=20)

#     # Image and button for Easy level
#     easy_img = Image.open("smileydog.jpg")  # Replace with your image path
#     easy_img = easy_img.resize((150, 150), Image.LANCZOS)
#     easy_photo = ImageTk.PhotoImage(easy_img)

#     easy_label = tk.Label(level_frame, image=easy_photo, bg="white")
#     easy_label.image = easy_photo
#     easy_label.grid(row=0, column=0, padx=30)

#     easy_button = tk.Button(level_frame, text="Start", command=show_main_screen, bg="green", fg="white", font=("Arial", 12))
#     easy_button.grid(row=1, column=0)

#     easy_text = tk.Label(level_frame, text="Easy", font=("Arial", 14), bg="white")
#     easy_text.grid(row=2, column=0, pady=10)

#     # Image and button for Medium level (Locked)
#     medium_img = Image.open("boy1.png")  # Replace with your image path
#     medium_img = medium_img.resize((150, 150), Image.LANCZOS)
#     medium_photo = ImageTk.PhotoImage(medium_img)

#     medium_label = tk.Label(level_frame, image=medium_photo, bg="white")
#     medium_label.image = medium_photo
#     medium_label.grid(row=0, column=1, padx=30)

#     medium_button = tk.Button(level_frame, text="Locked", state="disabled", bg="gray", fg="white", font=("Arial", 12))
#     medium_button.grid(row=1, column=1)

#     medium_text = tk.Label(level_frame, text="Medium", font=("Arial", 14), bg="white")
#     medium_text.grid(row=2, column=1, pady=10)

#     # Image and button for Hard level (Locked)
#     hard_img = Image.open("boy1.png")  # Replace with your image path
#     hard_img = hard_img.resize((150, 150), Image.LANCZOS)
#     hard_photo = ImageTk.PhotoImage(hard_img)

#     hard_label = tk.Label(level_frame, image=hard_photo, bg="white")
#     hard_label.image = hard_photo
#     hard_label.grid(row=0, column=2, padx=30)

#     hard_button = tk.Button(level_frame, text="Locked", state="disabled", bg="gray", fg="white", font=("Arial", 12))
#     hard_button.grid(row=1, column=2)

#     hard_text = tk.Label(level_frame, text="Hard", font=("Arial", 14), bg="white")
#     hard_text.grid(row=2, column=2, pady=10)

# # Create a loading screen with a background image and progress bar
# def loading_screen():
#     # Load and display the background image for the loading screen
#     bg_image = Image.open("boy.jpg")  # Replace with your background image path
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
#     bg_photo = ImageTk.PhotoImage(bg_image)
    
#     bg_label = tk.Label(root, image=bg_photo)
#     bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
#     bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Set the image to cover the full screen

#     load_label = tk.Label(root, text="Unlock Your Full Potential", font=("Arial", 40), fg="green", bg="lightblue")
#     load_label.pack(pady=200)

#     # Create the progress bar
#     progress_bar = tk.Canvas(root, width=400, height=30, bg="white", highlightthickness=0)
#     progress_bar.pack(pady=20)
#     load_progress = progress_bar.create_rectangle(0, 0, 0, 30, fill="green")

#     def fill_bar():
#         for i in range(1, 101):
#             progress_bar.coords(load_progress, (0, 0, i * 4, 30))
#             root.update_idletasks()
#             time.sleep(0.1)  # Simulate loading time

#         # Remove loading screen elements
#         load_label.destroy()
#         progress_bar.destroy()
#         bg_label.destroy()

#         # Show the level selection screen
#         game_levels_screen()

#     threading.Thread(target=fill_bar).start()

# # Start with the loading screen
# loading_screen()

# # Run the Tkinter event loop
# root.mainloop()


# import tkinter as tk
# from PIL import Image, ImageTk
# from TTS.api import TTS
# import threading
# import time
# import simpleaudio as sa
# import speech_recognition as sr
# from pydub import AudioSegment
# from pydub.effects import normalize, low_pass_filter
# import io

# # Initialize the main window
# root = tk.Tk()
# root.title("Game Level Selection")
# root.geometry("800x600")  # Set the window size
# root.configure(bg="white")

# # Initialize Coqui TTS
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_path="vocoder_models/en/ljspeech/hifigan_v2")

# # Lock to prevent speech overlap
# voice_lock = threading.Lock()

# # Initialize speech recognizer
# recognizer = sr.Recognizer()
# mic = sr.Microphone()

# # List of image paths and their corresponding texts (20 images)
# images_data = [
#     {"image_path": "all.jpg", "text": "This is a ball"},
#     {"image_path": "cat.jpg", "text": "This is a cat"},
#     {"image_path": "bed.jpg", "text": "This is a bed"},
#     {"image_path": "donkey.jpeg", "text": "This is a donkey"},
#     {"image_path": "owl.jpg", "text": "This is an owl"},
#     {"image_path": "bus(1).jpg", "text": "This is a bus"},
#     {"image_path": "bowl.jpg", "text": "This is a banana"},
#     {"image_path": "bell.jpg", "text": "This is a bell"},
#     {"image_path": "ball.jpg", "text": "This is a ball"},
#     {"image_path": "crocodile.jpg", "text": "This is a crocodile"},
#     {"image_path": "whiteduck.jpg", "text": "This is a white duck"},
#     {"image_path": "turtle.jpg", "text": "This is a turtle"},
#     {"image_path": "butterfly.jpg", "text": "This is a butterfly"},
#     {"image_path": "books.jpg", "text": "These are books"},
#     {"image_path": "duck.jpg", "text": "This is a duck"},
#     {"image_path": "bat.jpg", "text": "This is a bat"},
#     {"image_path": "monkey.jpg", "text": "This is a monkey"},
#     {"image_path": "zebra.jpg", "text": "This is a zebra"},
#     {"image_path": "fox.jpg", "text": "This is a fox"},
#     {"image_path": "boat.jpg", "text": "This is a boat"}
# ]

# # Variable to keep track of the current image index
# current_index = 0
# best_time = float('inf')

# # Function to use Coqui TTS to speak the text
# def speak_text(text):
#     with voice_lock:
#         print(f"Speaking: {text}")
#         tts.tts_to_file(text=text, file_path="tts_output.wav")
#         play_audio("tts_output.wav")

# # Function to play audio using simpleaudio
# def play_audio(filename):
#     wave_obj = sa.WaveObject.from_wave_file(filename)
#     play_obj = wave_obj.play()
#     play_obj.wait_done()

# # Function to resize the image while maintaining aspect ratio
# def resize_image(image, max_width, max_height):
#     img_width, img_height = image.size
#     ratio = min(max_width / img_width, max_height / img_height)
#     new_width = int(img_width * ratio)
#     new_height = int(img_height * ratio)
#     return image.resize((new_width, new_height), Image.LANCZOS)

# # Function to reduce noise and smooth the child's voice
# def process_audio_for_smoothing(audio_data):
#     # Convert the audio to an AudioSegment
#     audio_segment = AudioSegment(
#         data=audio_data.get_wav_data(),
#         sample_width=2,
#         frame_rate=audio_data.sample_rate,
#         channels=1
#     )

#     # Apply noise reduction and smoothing techniques
#     audio_segment = normalize(audio_segment)  # Normalize the volume
#     audio_segment = low_pass_filter(audio_segment, cutoff=3000)  # Low pass filter for smoother voice

#     # Convert back to byte data
#     byte_io = io.BytesIO()
#     audio_segment.export(byte_io, format="wav")
#     return byte_io.getvalue()

# # Function to listen for the child’s speech and time the response
# def listen_for_response(prompt, target_text):
#     global best_time
#     print(prompt)
#     speak_text(prompt)

#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source)
#         start_time = time.time()
#         print("Listening...")
#         audio = recognizer.listen(source, timeout=60)  # Listen for 60 seconds max

#     try:
#         print("Processing audio for noise reduction and smoothing...")
#         # Process the audio for noise reduction and smoothing
#         processed_audio = sr.AudioData(process_audio_for_smoothing(audio), audio.sample_rate, audio.sample_width)

#         print("Recognizing...")
#         speech_text = recognizer.recognize_google(processed_audio)
#         print(f"Child said: {speech_text}")
        
#         # Check if the child's response matches the expected text
#         if target_text.lower() in speech_text.lower():
#             elapsed_time = time.time() - start_time
#             print(f"Time taken: {elapsed_time:.2f} seconds")
            
#             # Check if the child improved their time
#             if elapsed_time < best_time and 40 <= elapsed_time <= 60:
#                 best_time = elapsed_time
#                 print("Improved! Moving to the next image.")
#                 next_image()
#             else:
#                 print("Try again!")
#         else:
#             print("Response doesn't match. Try again!")

#     except sr.UnknownValueError:
#         print("Sorry, I couldn't understand that. Please try again.")
#     except sr.RequestError as e:
#         print(f"Could not request results; {e}")

# # Function to update the displayed image and text
# def update_image():
#     global current_index
#     image_path = images_data[current_index]["image_path"]
#     instruction_text = images_data[current_index]["text"]
    
#     # Load and display the image
#     image = Image.open(image_path)
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
    
#     # Resize the image to fit the screen while maintaining the aspect ratio
#     image = resize_image(image, screen_width, screen_height)
#     photo = ImageTk.PhotoImage(image)
#     image_label.config(image=photo)
#     image_label.image = photo  # Keep a reference to avoid garbage collection

#     text_label.config(text=instruction_text)
#     text_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

#     # Speak the instruction and prompt for repetition
#     root.after(500, lambda: threading.Thread(target=handle_speech_interaction, args=(instruction_text,)).start())

# # Function to handle speaking and listening interaction
# def handle_speech_interaction(instruction_text):
#     speak_text(instruction_text)
#     time.sleep(1)  # Pause before prompting the child
#     listen_for_response("Repeat after me.", instruction_text)

# # Function to go to the next image
# def next_image():
#     global current_index
#     if current_index < len(images_data) - 1:
#         current_index += 1
#     else:
#         current_index = 0  # Loop back to the first image
#     update_image()

# # Function to go to the previous image
# def previous_image():
#     global current_index
#     if current_index > 0:
#         current_index -= 1
#     else:
#         current_index = len(images_data) - 1  # Loop back to the last image
#     update_image()

# # Function to switch from game level screen to main image display
# def show_main_screen():
#     for widget in root.winfo_children():
#         widget.destroy()  # Clear the current screen

#     # Create a label to display the image
#     global image_label
#     image_label = tk.Label(root)
#     image_label.pack(fill=tk.BOTH, expand=True)

#     # Create a label for the instruction text (overlay on image)
#     global text_label
#     text_label = tk.Label(root, text="", font=("Arial", 20), bg="white", fg="black")

#     # Create Previous and Next buttons
#     prev_button = tk.Button(root, text="Previous", font=("Arial", 14), bg="blue", fg="white", width=10, command=previous_image)
#     prev_button.place(relx=0.05, rely=0.9)  # Positioned at the left bottom corner

#     next_button = tk.Button(root, text="Next", font=("Arial", 14), bg="green", fg="white", width=10, command=next_image)
#     next_button.place(relx=0.85, rely=0.9)  # Positioned at the right bottom corner

#     # Initialize by showing the first image
#     update_image()

# # Function to create the game level selection screen
# def game_levels_screen():
#     # Title label
#     title_label = tk.Label(root, text="Game Levels", font=("Arial", 30), bg="white")
#     title_label.pack(pady=20)

#     # Create a frame for the game levels
#     level_frame = tk.Frame(root, bg="white")
#     level_frame.pack(pady=20)

#     # Easy level
#     easy_img = Image.open("smileydog.jpg")
#     easy_img = easy_img.resize((150, 150), Image.LANCZOS)
#     easy_photo = ImageTk.PhotoImage(easy_img)

#     easy_label = tk.Label(level_frame, image=easy_photo, bg="white")
#     easy_label.image = easy_photo
#     easy_label.grid(row=0, column=0, padx=30)

#     easy_button = tk.Button(level_frame, text="Start", command=show_main_screen, bg="green", fg="white", font=("Arial", 12))
#     easy_button.grid(row=1, column=0)

#     easy_text = tk.Label(level_frame, text="Easy", font=("Arial", 14), bg="white")
#     easy_text.grid(row=2, column=0, pady=10)

#     # Medium level
#     medium_img = Image.open("boy1.png")
#     medium_img = medium_img.resize((150, 150), Image.LANCZOS)
#     medium_photo = ImageTk.PhotoImage(medium_img)

#     medium_label = tk.Label(level_frame, image=medium_photo, bg="white")
#     medium_label.image = medium_photo
#     medium_label.grid(row=0, column=1, padx=30)

#     medium_button = tk.Button(level_frame, text="Locked", state="disabled", bg="gray", fg="white", font=("Arial", 12))
#     medium_button.grid(row=1, column=1)

#     medium_text = tk.Label(level_frame, text="Medium", font=("Arial", 14), bg="white")
#     medium_text.grid(row=2, column=1, pady=10)

#     # Hard level
#     hard_img = Image.open("boy1.png")
#     hard_img = hard_img.resize((150, 150), Image.LANCZOS)
#     hard_photo = ImageTk.PhotoImage(hard_img)

#     hard_label = tk.Label(level_frame, image=hard_photo, bg="white")
#     hard_label.image = hard_photo
#     hard_label.grid(row=0, column=2, padx=30)

#     hard_button = tk.Button(level_frame, text="Locked", state="disabled", bg="gray", fg="white", font=("Arial", 12))
#     hard_button.grid(row=1, column=2)

#     hard_text = tk.Label(level_frame, text="Hard", font=("Arial", 14), bg="white")
#     hard_text.grid(row=2, column=2, pady=10)

# # Create a loading screen with a background image and progress bar
# def loading_screen():
#     # Load and display the background image for the loading screen
#     bg_image = Image.open("boy.jpg")  # Replace with your background image path
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
#     bg_photo = ImageTk.PhotoImage(bg_image)
    
#     bg_label = tk.Label(root, image=bg_photo)
#     bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
#     bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Set the image to cover the full screen

#     load_label = tk.Label(root, text="Unlock Your Full Potential", font=("Arial", 40), fg="green", bg="lightblue")
#     load_label.pack(pady=200)

#     # Create the progress bar
#     progress_bar = tk.Canvas(root, width=400, height=30, bg="white", highlightthickness=0)
#     progress_bar.pack(pady=20)
#     load_progress = progress_bar.create_rectangle(0, 0, 0, 30, fill="green")

#     def fill_bar():
#         for i in range(1, 101):
#             progress_bar.coords(load_progress, (0, 0, i * 4, 30))
#             root.update_idletasks()
#             time.sleep(0.1)  # Simulate loading time

#         # Remove loading screen elements
#         load_label.destroy()
#         progress_bar.destroy()
#         bg_label.destroy()

#         # Show the level selection screen
#         game_levels_screen()

#     threading.Thread(target=fill_bar).start()

# # Start with the loading screen
# loading_screen()

# # Run the Tkinter event loop
# root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
# from TTS.api import TTS
# import threading
# import time
# import simpleaudio as sa
# import numpy as np
# import sounddevice as sd
# import speech_recognition as sr

# # Initialize the main window
# root = tk.Tk()
# root.title("Speech Game")
# root.geometry("800x600")
# root.configure(bg="white")

# # Initialize Coqui TTS
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_path="vocoder_models/en/ljspeech/hifigan_v2")

# # Initialize speech recognizer
# recognizer = sr.Recognizer()

# # List of image paths and their corresponding texts
# images_data = [
#     {"image_path": "all.jpg", "text": "This is a ball"},
#     {"image_path": "cat.jpg", "text": "This is a cat"},
#     {"image_path": "bed.jpg", "text": "This is a bed"},
#     {"image_path": "donkey.jpeg", "text": "This is a donkey"}
# ]

# # Variables for tracking current image and recording
# current_index = 0
# audio_data = []
# start_time = 0

# # Dynamic feedback messages
# success_feedbacks = [
#     "Great job! You were really quick!",
#     "Awesome work! You completed it in time.",
#     "Well done! You said it perfectly.",
#     "Excellent! You're improving!"
# ]
# retry_feedbacks = [
#     "Don't worry, you'll get faster!",
#     "Keep trying, you're almost there!",
#     "Try again, and aim to be quicker.",
#     "Keep it up! You can do this."
# ]

# # Function to use Coqui TTS to speak the text
# def speak_text(text):
#     tts.tts_to_file(text=text, file_path="tts_output.wav")
#     play_audio("tts_output.wav")

# # Function to play audio using simpleaudio
# def play_audio(filename):
#     try:
#         wave_obj = sa.WaveObject.from_wave_file(filename)
#         play_obj = wave_obj.play()  # Start playing the audio
#         play_obj.wait_done()  # Wait until the audio finishes
#     except Exception as e:
#         print(f"Audio playback error: {e}")

# # Function to resize the image while maintaining aspect ratio
# def resize_image(image, max_width, max_height):
#     img_width, img_height = image.size
#     ratio = min(max_width / img_width, max_height / img_height)
#     return image.resize((int(img_width * ratio), int(img_height * ratio)), Image.LANCZOS)

# # Function to update the displayed image and text
# def update_image():
#     global current_index
#     image_path = images_data[current_index]["image_path"]
#     instruction_text = images_data[current_index]["text"]

#     # Load and display the image
#     image = Image.open(image_path)
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     image = resize_image(image, screen_width, screen_height)
#     photo = ImageTk.PhotoImage(image)
#     image_label.config(image=photo)
#     image_label.image = photo

#     text_label.config(text=instruction_text)
#     text_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

#     # Start TTS and automatic recording after a short delay
#     root.after(500, lambda: threading.Thread(target=handle_speech_interaction, args=(instruction_text,)).start())

# # Function to handle speaking and automatic recording interaction
# def handle_speech_interaction(instruction_text):
#     speak_text(instruction_text)
#     time.sleep(1)  # Pause before starting the recording
#     start_recording()

# # Function to start recording
# def start_recording():
#     global start_time, audio_data
#     start_time = time.time()  # Initialize start time
#     audio_data = []  # Clear previous data

#     try:
#         fs = 44100  # Sample rate
#         duration = 10  # Max recording duration (for safety, not fixed to 40s)
#         print("Recording... Speak now!")

#         # Start recording
#         audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
#         sd.wait()  # Wait until recording is finished or stopped

#         elapsed_time = time.time() - start_time  # Measure elapsed time
#         analyze_speech(elapsed_time)

#     except Exception as e:
#         print(f"Recording error: {e}")
#         feedback_label.config(text="Error in recording, please try again.")

# # Function to analyze speech duration and provide feedback
# def analyze_speech(elapsed_time):
#     if elapsed_time <= 40:
#         feedback = np.random.choice(success_feedbacks)
#         feedback_label.config(text=f"{feedback}\nYou took {elapsed_time:.2f} seconds.")
#         speak_text(feedback)  # Speak the success message using TTS
#         root.after(4000, next_image)  # Move to the next image after feedback
#     else:
#         feedback = np.random.choice(retry_feedbacks)
#         feedback_label.config(text=f"{feedback}\nYou took {elapsed_time:.2f} seconds.")
#         speak_text(feedback)  # Speak the retry message using TTS
#         root.after(4000, update_image)  # Retry the same image

# # Function to go to the next image
# def next_image():
#     global current_index
#     if current_index < len(images_data) - 1:
#         current_index += 1
#     else:
#         current_index = 0  # Loop back to the first image
#     update_image()

# # Initialize the main screen
# image_label = tk.Label(root)
# image_label.pack(fill=tk.BOTH, expand=True)

# text_label = tk.Label(root, text="", font=("Arial", 20), bg="white", fg="black")
# feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="white", fg="black")
# feedback_label.pack(pady=10)

# # Start by showing the first image
# update_image()

# # Run the Tkinter main loop
# root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
# from TTS.api import TTS
# import threading
# import time
# import simpleaudio as sa
# import numpy as np
# import sounddevice as sd

# # Initialize the main window
# root = tk.Tk()
# root.title("Speech Game")
# root.attributes('-fullscreen', True)  # Make the window fullscreen
# root.configure(bg="white")

# # Initialize Coqui TTS
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_path="vocoder_models/en/ljspeech/hifigan_v2")

# # Variables for tracking current image and recording
# current_index = 0
# stars_earned = 0  # Star counter

# # List of image paths and their corresponding texts
# images_data = [
#     {"image_path": "all.jpg", "text": "This is a ball"},
#     {"image_path": "cat.jpg", "text": "This is a cat"},
#     {"image_path": "bed.jpg", "text": "This is a bed"},
#     {"image_path": "donkey.jpeg", "text": "This is a donkey"}
# ]

# # Success and retry messages
# success_feedbacks = [
#     "Great job! You were really quick!",
#     "Awesome work! You completed it in time.",
#     "Well done! You said it perfectly.",
#     "Excellent! You're improving!"
# ]
# retry_feedbacks = [
#     "Don't worry, you'll get faster!",
#     "Keep trying, you're almost there!",
#     "Try again, and aim to be quicker.",
#     "Keep it up! You can do this."
# ]

# # Function to use Coqui TTS to speak the text
# def speak_text(text):
#     try:
#         tts.tts_to_file(text=text, file_path="tts_output.wav")
#         play_audio("tts_output.wav")
#     except Exception as e:
#         print(f"TTS error: {e}")

# # Function to play audio using simpleaudio
# def play_audio(filename):
#     try:
#         wave_obj = sa.WaveObject.from_wave_file(filename)
#         play_obj = wave_obj.play()
#         play_obj.wait_done()  # Wait until the audio finishes
#     except Exception as e:
#         print(f"Audio playback error: {e}")

# # Loading screen
# def loading_screen():
#     for widget in root.winfo_children():
#         widget.destroy()

#     # Load the background image for loading screen
#     bg_image = Image.open("boy.jpg")  # Replace with the actual image path
#     bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
#     bg_photo = ImageTk.PhotoImage(bg_image)

#     bg_label = tk.Label(root, image=bg_photo)
#     bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
#     bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#     load_label = tk.Label(root, text="Unlock Your Full Potential", font=("Arial", 40), fg="green", bg="lightblue")
#     load_label.pack(pady=200)

#     progress_bar = tk.Canvas(root, width=400, height=30, bg="white", highlightthickness=0)
#     progress_bar.pack(pady=20)
#     load_progress = progress_bar.create_rectangle(0, 0, 0, 30, fill="green")

#     def fill_bar():
#         for i in range(1, 101):
#             progress_bar.coords(load_progress, (0, 0, i * 4, 30))
#             root.update_idletasks()
#             time.sleep(0.05)

#         bg_label.destroy()
#         load_label.destroy()
#         progress_bar.destroy()
#         game_levels_screen()

#     threading.Thread(target=fill_bar).start()

# # Game level selection screen
# def game_levels_screen():
#     for widget in root.winfo_children():
#         widget.destroy()

#     title_label = tk.Label(root, text="Game Levels", font=("Arial", 30), bg="white")
#     title_label.pack(pady=20)

#     level_frame = tk.Frame(root, bg="white")
#     level_frame.pack(pady=20)

#     # Easy level with image
#     easy_img = Image.open("smileydog.jpg")  # Replace with the actual image path
#     easy_img = easy_img.resize((150, 150), Image.LANCZOS)
#     easy_photo = ImageTk.PhotoImage(easy_img)

#     easy_label = tk.Label(level_frame, image=easy_photo, bg="white")
#     easy_label.image = easy_photo
#     easy_label.grid(row=0, column=0, padx=30)

#     easy_button = tk.Button(level_frame, text="Start", command=show_main_screen, bg="green", fg="white", font=("Arial", 12))
#     easy_button.grid(row=1, column=0, pady=10)

#     easy_text = tk.Label(level_frame, text="Easy Level", font=("Arial", 14), bg="white")
#     easy_text.grid(row=2, column=0, pady=10)

# # Show the main screen with images and text
# def show_main_screen():
#     for widget in root.winfo_children():
#         widget.destroy()

#     global image_label, text_label, feedback_label, stars_label

#     image_label = tk.Label(root)
#     image_label.pack(expand=True)

#     text_label = tk.Label(root, text="", font=("Arial", 24), bg="white", fg="black")
#     text_label.pack(pady=20)

#     stars_label = tk.Label(root, text=f"★ {stars_earned}", font=("Arial", 14), bg="white", fg="black")
#     stars_label.pack(pady=5)

#     feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="white", fg="black")
#     feedback_label.pack(pady=10)

#     update_image()  # Start showing images

# # Function to update the displayed image and text
# def update_image():
#     global current_index

#     try:
#         image_path = images_data[current_index]["image_path"]
#         instruction_text = images_data[current_index]["text"]

#         image = Image.open(image_path)
#         image = image.resize((600, 400), Image.LANCZOS)  # Adjust size for fullscreen display
#         photo = ImageTk.PhotoImage(image)
#         image_label.config(image=photo)
#         image_label.image = photo

#         text_label.config(text=instruction_text)

#         # Start TTS and speech interaction after a short delay
#         root.after(500, lambda: threading.Thread(target=handle_speech_interaction, args=(instruction_text,)).start())

#     except Exception as e:
#         print(f"Image loading error: {e}")

# # Function to handle speaking and automatic recording interaction
# def handle_speech_interaction(instruction_text):
#     try:
#         speak_text(instruction_text)
#         time.sleep(1)
#         speak_text("Repeat after me.")
#         time.sleep(1)
#         start_recording()
#     except Exception as e:
#         print(f"Speech interaction error: {e}")

# # Function to start recording
# def start_recording():
#     try:
#         fs = 44100  # Sample rate
#         duration = 5  # Max recording duration
#         print("Recording... Speak now!")

#         audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
#         sd.wait()

#         elapsed_time = 3.5  # Mock elapsed time for testing
#         root.after(0, lambda: analyze_speech(elapsed_time))

#     except Exception as e:
#         root.after(0, lambda: feedback_label.config(text="Error in recording, please try again."))
#         print(f"Recording error: {e}")

# # Function to analyze speech duration and provide feedback
# def analyze_speech(elapsed_time):
#     global stars_earned

#     if elapsed_time <= 40:
#         feedback = np.random.choice(success_feedbacks)
#         stars_earned += 1
#         stars_label.config(text=f"★ {stars_earned}")
#         speak_text(feedback)  # Speak out the feedback
#         root.after(4000, next_image)  # Move to the next image after feedback
#     else:
#         feedback = np.random.choice(retry_feedbacks)
#         speak_text(feedback)  # Speak out the retry feedback
#         root.after(4000, update_image)  # Retry the same image

# # Function to go to the next image
# def next_image():
#     global current_index
#     if current_index < len(images_data) - 1:
#         current_index += 1
#     else:
#         current_index = 0  # Loop back to the first image
#     update_image()

# # Start with the loading screen
# loading_screen()

# # Run the Tkinter main loop
# root.mainloop()

# import tkinter as tk
# from PIL import Image, ImageTk
# from TTS.api import TTS
# import threading
# import time
# import simpleaudio as sa
# import numpy as np
# import sounddevice as sd
# import random

# # Initialize the main window
# root = tk.Tk()
# root.title("Speech Game")
# root.attributes('-fullscreen', True)  # Make the window fullscreen
# root.configure(bg="white")

# # Initialize Coqui TTS
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_path="vocoder_models/en/ljspeech/hifigan_v2")

# # Variables for tracking current image and recording
# current_index = 0
# stars_earned = 0  # Star counter

# # List of image paths and their corresponding texts
# images_data = [
#     {"image_path": "all.jpg", "text": "This is a ball"},
#     {"image_path": "cat.jpg", "text": "This is a cat"},
#     {"image_path": "bed.jpg", "text": "This is a bed"},
#     {"image_path": "donkey.jpeg", "text": "This is a donkey"}
# ]

# # Success and retry messages
# success_feedbacks = [
#     "Great job! You were really quick!",
#     "Awesome work! You completed it in time.",
#     "Well done! You said it perfectly.",
#     "Excellent! You're improving!"
# ]
# retry_feedbacks = [
#     "Don't worry, you'll get faster!",
#     "Keep trying, you're almost there!",
#     "Try again, and aim to be quicker.",
#     "Keep it up! You can do this."
# ]

# # Function to use Coqui TTS to speak the text
# def speak_text(text):
#     try:
#         tts.tts_to_file(text=text, file_path="tts_output.wav")
#         play_audio("tts_output.wav")
#     except Exception as e:
#         print(f"TTS error: {e}")

# # Function to play audio using simpleaudio
# def play_audio(filename):
#     try:
#         wave_obj = sa.WaveObject.from_wave_file(filename)
#         play_obj = wave_obj.play()
#         play_obj.wait_done()  # Wait until the audio finishes
#     except Exception as e:
#         print(f"Audio playback error: {e}")

# # Loading screen
# def loading_screen():
#     for widget in root.winfo_children():
#         widget.destroy()

#     # Load the background image for loading screen
#     bg_image = Image.open("boy.jpg")  # Replace with the actual image path
#     bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
#     bg_photo = ImageTk.PhotoImage(bg_image)

#     bg_label = tk.Label(root, image=bg_photo)
#     bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
#     bg_label.place(x=0, y=0, relwidth=1, relheight=1)

#     load_label = tk.Label(root, text="Unlock Your Full Potential", font=("Arial", 40), fg="green", bg="lightblue")
#     load_label.pack(pady=200)

#     progress_bar = tk.Canvas(root, width=400, height=30, bg="white", highlightthickness=0)
#     progress_bar.pack(pady=20)
#     load_progress = progress_bar.create_rectangle(0, 0, 0, 30, fill="green")

#     def fill_bar():
#         for i in range(1, 101):
#             progress_bar.coords(load_progress, (0, 0, i * 4, 30))
#             root.update_idletasks()
#             time.sleep(0.05)

#         bg_label.destroy()
#         load_label.destroy()
#         progress_bar.destroy()
#         game_levels_screen()

#     threading.Thread(target=fill_bar).start()

# # Game level selection screen
# def game_levels_screen():
#     for widget in root.winfo_children():
#         widget.destroy()

#     title_label = tk.Label(root, text="Game Levels", font=("Arial", 30), bg="white")
#     title_label.pack(pady=20)

#     level_frame = tk.Frame(root, bg="white")
#     level_frame.pack(expand=True)

#     levels_data = [
#         {"image": "smileydog.jpg", "name": "Easy Level", "command": show_main_screen},
#         {"image": "boy1.png", "name": "Medium Level", "command": show_main_screen},
#         {"image": "boy2.png", "name": "Hard Level", "command": show_main_screen}
#     ]

#     for index, level in enumerate(levels_data):
#         img = Image.open(level["image"])
#         img = img.resize((200, 200), Image.LANCZOS)  # Make images bigger
#         photo = ImageTk.PhotoImage(img)

#         level_label = tk.Label(level_frame, image=photo, bg="white")
#         level_label.image = photo
#         level_label.grid(row=0, column=index, padx=20, pady=10)

#         level_button = tk.Button(level_frame, text=level["name"], command=level["command"], 
#                                  bg="green", fg="white", font=("Arial", 14))
#         level_button.grid(row=1, column=index, pady=10)

# # Show the main screen with images and text
# def show_main_screen():
#     for widget in root.winfo_children():
#         widget.destroy()

#     global image_label, text_label, feedback_label, stars_label

#     image_label = tk.Label(root)
#     image_label.pack(expand=True)

#     text_label = tk.Label(root, text="", font=("Arial", 24), bg="white", fg="black")
#     text_label.pack(pady=20)

#     stars_label = tk.Label(root, text=f"★ {stars_earned}", font=("Arial", 14), bg="white", fg="black")
#     stars_label.pack(pady=5)

#     feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="white", fg="black")
#     feedback_label.pack(pady=10)

#     update_image()  # Start showing images

# # Function to update the displayed image and text
# def update_image():
#     global current_index

#     try:
#         image_path = images_data[current_index]["image_path"]
#         instruction_text = images_data[current_index]["text"]

#         image = Image.open(image_path)
#         image = image.resize((800, 500), Image.LANCZOS)  # Make images bigger
#         photo = ImageTk.PhotoImage(image)
#         image_label.config(image=photo)
#         image_label.image = photo

#         text_label.config(text=instruction_text)

#         # Start TTS and speech interaction after a short delay
#         root.after(500, lambda: threading.Thread(target=handle_speech_interaction, args=(instruction_text,)).start())

#     except Exception as e:
#         print(f"Image loading error: {e}")

# # Function to handle speaking and automatic recording interaction
# def handle_speech_interaction(instruction_text):
#     try:
#         speak_text(instruction_text)
#         time.sleep(1)
#         speak_text("Repeat after me.")
#         time.sleep(1)
#         start_recording()
#     except Exception as e:
#         print(f"Speech interaction error: {e}")

# # Function to start recording
# def start_recording():
#     try:
#         fs = 44100  # Sample rate
#         duration = 5  # Max recording duration
#         print("Recording... Speak now!")

#         audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
#         sd.wait()

#         elapsed_time = 3.5  # Mock elapsed time for testing
#         root.after(0, lambda: analyze_speech(elapsed_time))

#     except Exception as e:
#         root.after(0, lambda: feedback_label.config(text="Error in recording, please try again."))
#         print(f"Recording error: {e}")

# # Function to create multiple star pop-up effects
# def animate_star_effect():
#     for _ in range(30):  # Create 30 stars
#         x_pos = random.uniform(0.1, 0.9)
#         y_pos = random.uniform(0.1, 0.9)
#         star_label = tk.Label(root, text="★", font=("Arial", 24), fg="gold", bg="white")
#         star_label.place(relx=x_pos, rely=y_pos, anchor="center")

#         # Animate star fading away
#         def fade_star(star_label):
#             for size in range(24, 1, -1):
#                 star_label.config(font=("Arial", size))
#                 root.update_idletasks()
#                 time.sleep(0.03)
#             star_label.destroy()

#         threading.Thread(target=fade_star, args=(star_label,), daemon=True).start()

# # Function to analyze speech duration and provide feedback
# def analyze_speech(elapsed_time):
#     global stars_earned

#     if elapsed_time <= 40:
#         feedback = np.random.choice(success_feedbacks)
#         stars_earned += 1
#         stars_label.config(text=f"★ {stars_earned}")
#         speak_text(feedback)  # Speak out the feedback
#         threading.Thread(target=animate_star_effect).start()  # Show multiple stars pop-up effect
#         root.after(4000, next_image)  # Move to the next image after feedback
#     else:
#         feedback = np.random.choice(retry_feedbacks)
#         speak_text(feedback)  # Speak out the retry feedback
#         root.after(4000, update_image)  # Retry the same image

# # Function to go to the next image
# def next_image():
#     global current_index
#     if current_index < len(images_data) - 1:
#         current_index += 1
#     else:
#         current_index = 0  # Loop back to the first image
#     update_image()

# # Start with the loading screen
# loading_screen()

# # Run the Tkinter main loop
# root.mainloop()

import tkinter as tk
from PIL import Image, ImageTk
from TTS.api import TTS
import threading
import time
import simpleaudio as sa
import numpy as np
import sounddevice as sd
import random

# Initialize the main window
root = tk.Tk()
root.title("Speech Game")
root.attributes('-fullscreen', True)  # Make the window fullscreen
root.configure(bg="white")

# Initialize Coqui TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", vocoder_path="vocoder_models/en/ljspeech/hifigan_v2")

# Variables for tracking current image and recording
current_index = 0
stars_earned = 0  # Star counter

# List of image paths and their corresponding texts
images_data = [
    {"image_path": "all.jpg", "text": "This is a ball"},
    {"image_path": "cat.jpg", "text": "This is a cat"},
    {"image_path": "bed.jpg", "text": "This is a bed"},
    {"image_path": "donkey.jpeg", "text": "This is a donkey"}
]

# Success and retry messages
success_feedbacks = [
    "Great job! You were really quick!",
    "Awesome work! You completed it in time.",
    "Well done! You said it perfectly.",
    "Excellent! You're improving!"
]
retry_feedbacks = [
    "Don't worry, you'll get faster!",
    "Keep trying, you're almost there!",
    "Try again, and aim to be quicker.",
    "Keep it up! You can do this."
]

# Function to use Coqui TTS to speak the text
def speak_text(text):
    try:
        tts.tts_to_file(text=text, file_path="tts_output.wav")
        play_audio("tts_output.wav")
    except Exception as e:
        print(f"TTS error: {e}")

# Function to play audio using simpleaudio
def play_audio(filename):
    try:
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until the audio finishes
    except Exception as e:
        print(f"Audio playback error: {e}")

# Loading screen
def loading_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Load the background image for loading screen
    bg_image = Image.open("boy.jpg")  # Replace with the actual image path
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    load_label = tk.Label(root, text="Unlock Your Full Potential", font=("Arial", 40), fg="green", bg="lightblue")
    load_label.pack(pady=200)

    progress_bar = tk.Canvas(root, width=400, height=30, bg="white", highlightthickness=0)
    progress_bar.pack(pady=20)
    load_progress = progress_bar.create_rectangle(0, 0, 0, 30, fill="green")

    def fill_bar():
        for i in range(1, 101):
            progress_bar.coords(load_progress, (0, 0, i * 4, 30))
            root.update_idletasks()
            time.sleep(0.05)

        bg_label.destroy()
        load_label.destroy()
        progress_bar.destroy()
        game_levels_screen()

    threading.Thread(target=fill_bar).start()

# Game level selection screen
def game_levels_screen():
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(root, text="Game Levels", font=("Arial", 30), bg="white")
    title_label.pack(pady=20)

    level_frame = tk.Frame(root, bg="white")
    level_frame.pack(expand=True)

    levels_data = [
        {"image": "smileydog.jpg", "name": "Easy Level", "command": show_main_screen},
        {"image": "boy1.png", "name": "Medium Level", "command": show_main_screen},
        {"image": "boy2.png", "name": "Hard Level", "command": show_main_screen}
    ]

    for index, level in enumerate(levels_data):
        img = Image.open(level["image"])
        img = img.resize((200, 200), Image.LANCZOS)  # Make images bigger
        photo = ImageTk.PhotoImage(img)

        level_label = tk.Label(level_frame, image=photo, bg="white")
        level_label.image = photo
        level_label.grid(row=0, column=index, padx=20, pady=10)

        level_button = tk.Button(level_frame, text=level["name"], command=level["command"], 
                                 bg="green", fg="white", font=("Arial", 14))
        level_button.grid(row=1, column=index, pady=10)

# Show the main screen with images and text
def show_main_screen():
    for widget in root.winfo_children():
        widget.destroy()

    global image_label, text_label, feedback_label, stars_label

    image_label = tk.Label(root)
    image_label.pack(expand=True)

    text_label = tk.Label(root, text="", font=("Arial", 24), bg="white", fg="black")
    text_label.pack(pady=20)

    stars_label = tk.Label(root, text=f"★ {stars_earned}", font=("Arial", 14), bg="white", fg="black")
    stars_label.pack(pady=5)

    feedback_label = tk.Label(root, text="", font=("Helvetica", 14), bg="white", fg="black")
    feedback_label.pack(pady=10)

    update_image()  # Start showing images

# Function to update the displayed image and text
def update_image():
    global current_index

    try:
        image_path = images_data[current_index]["image_path"]
        instruction_text = images_data[current_index]["text"]

        image = Image.open(image_path)
        image = image.resize((800, 500), Image.LANCZOS)  # Make images bigger
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

        text_label.config(text=instruction_text)

        # Start TTS and speech interaction after a short delay
        root.after(500, lambda: threading.Thread(target=handle_speech_interaction, args=(instruction_text,)).start())

    except Exception as e:
        print(f"Image loading error: {e}")

# Function to handle speaking and automatic recording interaction
def handle_speech_interaction(instruction_text):
    try:
        speak_text(instruction_text)
        time.sleep(1)
        speak_text("Repeat after me.")
        time.sleep(1)
        start_recording()
    except Exception as e:
        print(f"Speech interaction error: {e}")

# Function to start recording
def start_recording():
    try:
        fs = 44100  # Sample rate
        duration = 5  # Max recording duration
        print("Recording... Speak now!")

        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
        sd.wait()

        elapsed_time = 3.5  # Mock elapsed time for testing
        root.after(0, lambda: analyze_speech(elapsed_time))

    except Exception as e:
        root.after(0, lambda: feedback_label.config(text="Error in recording, please try again."))
        print(f"Recording error: {e}")

# Function to create multiple star pop-up effects
def animate_star_effect():
    for _ in range(50):  # Create 50 stars
        x_pos = random.uniform(0.1, 0.9)
        y_pos = random.uniform(0.1, 0.9)
        star_label = tk.Label(root, text="★", font=("Arial", 24), fg="gold", bg="white")
        star_label.place(relx=x_pos, rely=y_pos, anchor="center")

        # Animate star staying for 2 seconds before fading
        def fade_star(star_label):
            time.sleep(2)  # Star stays for 2 seconds
            for size in range(24, 1, -1):
                star_label.config(font=("Arial", size))
                root.update_idletasks()
                time.sleep(0.03)
            star_label.destroy()

        threading.Thread(target=fade_star, args=(star_label,), daemon=True).start()

# Function to analyze speech duration and provide feedback
def analyze_speech(elapsed_time):
    global stars_earned

    if elapsed_time <= 40:
        feedback = np.random.choice(success_feedbacks)
        stars_earned += 1
        stars_label.config(text=f"★ {stars_earned}")
        speak_text(feedback)  # Speak out the feedback
        threading.Thread(target=animate_star_effect).start()  # Show multiple stars pop-up effect
        root.after(4000, next_image)  # Move to the next image after feedback
    else:
        feedback = np.random.choice(retry_feedbacks)
        speak_text(feedback)  # Speak out the retry feedback
        root.after(4000, update_image)  # Retry the same image

# Function to go to the next image
def next_image():
    global current_index
    if current_index < len(images_data) - 1:
        current_index += 1
    else:
        current_index = 0  # Loop back to the first image
    update_image()

# Start with the loading screen
loading_screen()

# Run the Tkinter main loop
root.mainloop()
