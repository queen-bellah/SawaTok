import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import time

# Initialize the TTS engine (Text-to-Speech)
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Set speech rate
tts_engine.setProperty('volume', 1)  # Set volume level

# Initialize the recognizer for speech recognition (PocketSphinx)
recognizer = sr.Recognizer()

# Variables for timing
start_time = 0

# Function for TTS (Text-to-Speech)
def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function for Speech Recognition (Offline using PocketSphinx)
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

        try:
            recognized_text = recognizer.recognize_sphinx(audio)
            return recognized_text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

# Function to track and analyze the child's response time
def analyze_response_time(elapsed_time):
    if elapsed_time <= 10:
        return "Great job! That's the best response!"
    elif 11 <= elapsed_time <= 20:
        return "Good job! You're in the normal range!"
    elif 21 <= elapsed_time <= 40:
        return "Mild stuttering, but you're doing well!"
    elif 41 <= elapsed_time <= 60:
        return "Moderate stuttering, let's try again!"
    else:
        return "Severe stuttering, please repeat the word."

# Function for starting the speech test and tracking the child's response time
def start_speech_test(word):
    global start_time
    speak_text(f"Please say: {word}")
    start_time = time.time()  # Start time tracking

def stop_speech_test(word):
    global start_time
    elapsed_time = time.time() - start_time  # Calculate elapsed time
    recognized_text = recognize_speech()

    if recognized_text.lower() == word.lower():
        feedback = analyze_response_time(elapsed_time)
    else:
        feedback = "Try again, I couldn't understand you."

    speak_text(feedback)
    print(feedback)

# GUI setup using Tkinter
class StutteringToyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stuttering Therapy Toy")

        # Input words and their corresponding images for each module
        self.modules = {
            "Severe Stuttering": [
                ("Dog", "all.jpg"), 
                ("Ball", "babbyboss.jpg"),
                ("Apple", "bag.jpg"),
                ("Cat", "banana.jpg"),
                ("Book", "book.jpg"),
            ],
            "Moderate Stuttering": [
                ("The dog is running", "box.jpg"), 
                ("The ball is red", "bus.jpg"),
                ("I have an apple", "cat.jpg"),
            ],
            "Mild Stuttering": [
                ("How was your day?", "cutecat.jpg"), 
                ("Tell me about your school", "dogs.jpg"),
            ],
        }

        self.current_module = "Severe Stuttering"
        self.current_word = ""
        self.current_image = None

        # Create GUI elements
        self.label = tk.Label(root, text="Welcome to Stuttering Therapy Toy", font=("Arial", 16))
        self.label.pack(pady=20)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Module", command=self.start_module)
        self.start_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next Word", command=self.next_word, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Test", command=self.stop_test, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def start_module(self):
        self.current_module = "Severe Stuttering"  # Starting with the first module
        self.word_index = 0
        self.next_word()

    def next_word(self):
        if self.word_index < len(self.modules[self.current_module]):
            self.current_word, image_path = self.modules[self.current_module][self.word_index]
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.image)
            self.label.config(text=f"Say: {self.current_word}")

            start_speech_test(self.current_word)
            self.next_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.word_index += 1
        else:
            self.label.config(text="Module completed!")

    def stop_test(self):
        stop_speech_test(self.current_word)
        self.next_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

# Start the GUI
root = tk.Tk()
app = StutteringToyApp(root)
root.mainloop()
