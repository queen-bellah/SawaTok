import tkinter as tk
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time
import threading
import soundfile as sf

# Global variables
recording = False
audio_data = []
start_time = 0
timer_thread = None
recording_thread = None

# Tkinter window
root = tk.Tk()
root.title("Voice Recording & Feedback")

# Label to show feedback
feedback_label = tk.Label(root, text="Press 'Start Recording' to begin", font=("Helvetica", 14))
feedback_label.pack(pady=20)

# Function to start recording in a separate thread
def start_recording_thread():
    global recording, start_time, audio_data, timer_thread
    feedback_label.config(text="Good job! Recording...")  # Immediate feedback
    start_time = time.time()  # Start the timer
    audio_data = []  # Clear any previous data
    recording = True
    sd.default.samplerate = 44100
    sd.default.channels = 1
    stream = sd.InputStream(callback=audio_callback)

    # Start recording in a separate thread to avoid blocking the UI
    timer_thread = threading.Thread(target=update_timer)
    timer_thread.start()

    with stream:
        sd.sleep(5000)  # Record for 5 seconds or adjust as needed

    stop_recording()

# Function to handle starting the recording
def start_recording():
    global recording_thread
    recording_thread = threading.Thread(target=start_recording_thread)
    recording_thread.start()

# Function to stop recording and analyze the audio
def stop_recording():
    global recording
    recording = False
    end_time = time.time()  # Stop the timer
    duration = end_time - start_time  # Calculate the duration of speech
    analyze_audio(duration)
    play_recording()  # Play back the recorded audio

# Callback function to capture audio data
def audio_callback(indata, frames, time, status):
    global audio_data
    if recording:
        audio_data.append(indata.copy())

# Function to update the timer during recording
def update_timer():
    while recording:
        elapsed_time = time.time() - start_time
        feedback_label.config(text=f"Recording... Time: {elapsed_time:.2f} seconds")
        time.sleep(0.1)

# Function to analyze the audio and provide feedback
def analyze_audio(duration):
    global audio_data
    # Convert recorded audio to numpy array
    audio = np.concatenate(audio_data, axis=0)
    
    # Simple analysis based on duration (you can expand this to more complex analysis)
    if duration < 1.5:  # Threshold for short response
        feedback_label.config(text="Try speaking longer. Your time: {:.2f} seconds".format(duration))
    elif duration > 3.0:  # Threshold for long response
        feedback_label.config(text="Good job! Your time: {:.2f} seconds".format(duration))
    else:
        feedback_label.config(text="Well done! Your time: {:.2f} seconds".format(duration))
    
    # Save the audio to a file if needed
    write("output.wav", 44100, np.asarray(audio))  # Save the recording as a WAV file

# Function to play back the recorded audio
def play_recording():
    feedback_label.config(text="Playing your recording...")
    data, fs = sf.read("output.wav")  # Read the saved file
    sd.play(data, fs)
    sd.wait()  # Wait for the playback to finish
    feedback_label.config(text="Finished playing your recording.")

# Buttons to start and stop recording
start_button = tk.Button(root, text="Start Recording", command=start_recording, font=("Helvetica", 14))
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, font=("Helvetica", 14))
stop_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()















