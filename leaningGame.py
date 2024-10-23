import tkinter as tk
from PIL import Image, ImageTk, ImageSequence  # Added ImageSequence import
from TTS.api import TTS
import threading
import time
import wave
import pyaudio
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment
from pydub.effects import normalize, low_pass_filter
import io
import os
import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechEngine:
    def __init__(self):
        try:
            self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
            self.recognizer = sr.Recognizer()
            self.mic = sr.Microphone()
            
            # Adjust for ambient noise initially
            with self.mic as source:
                logger.info("Calibrating for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            self.voice_lock = threading.Lock()
            self.is_listening = False
            
        except Exception as e:
            logger.error(f"Error initializing speech engine: {e}")
            raise

    def speak(self, text):
        """Generate and play speech from text"""
        try:
            with self.voice_lock:
                logger.info(f"Speaking: {text}")
                temp_file = "temp_speech.wav"
                self.tts.tts_to_file(text=text, file_path=temp_file)
                
                # Play audio
                with wave.open(temp_file, 'rb') as wf:
                    p = pyaudio.PyAudio()
                    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                  channels=wf.getnchannels(),
                                  rate=wf.getframerate(),
                                  output=True)
                    
                    chunk_size = 1024
                    data = wf.readframes(chunk_size)
                    
                    while data:
                        stream.write(data)
                        data = wf.readframes(chunk_size)
                    
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                
                # Clean up temp file
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
        except Exception as e:
            logger.error(f"Error in speech synthesis: {e}")

    def listen_with_timeout(self, timeout=40):
        """Listen for speech with timeout and return (text, time_taken)"""
        try:
            with self.mic as source:
                logger.info("Listening for speech...")
                self.is_listening = True
                start_time = time.time()
                
                try:
                    audio = self.recognizer.listen(source, timeout=timeout)
                    time_taken = time.time() - start_time
                    
                    # Process audio for better recognition
                    processed_audio = self._process_audio(audio)
                    
                    text = self.recognizer.recognize_google(processed_audio)
                    logger.info(f"Recognized: {text} (Time taken: {time_taken:.2f}s)")
                    return text.lower(), time_taken
                    
                except sr.WaitTimeoutError:
                    time_taken = timeout
                    logger.info("Listening timeout reached")
                    return None, time_taken
                    
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None, timeout
        finally:
            self.is_listening = False

    def _process_audio(self, audio_data):
        """Process audio for better recognition quality"""
        try:
            audio_segment = AudioSegment(
                data=audio_data.get_wav_data(),
                sample_width=audio_data.sample_width,
                frame_rate=audio_data.sample_rate,
                channels=1
            )
            
            processed = normalize(audio_segment)
            processed = low_pass_filter(processed, 3000)
            
            buffer = io.BytesIO()
            processed.export(buffer, format="wav")
            
            return sr.AudioData(
                buffer.getvalue(),
                sample_rate=audio_data.sample_rate,
                sample_width=audio_data.sample_width
            )
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return audio_data

class GifPlayer:
    def __init__(self, gif_label, gif_path):
        self.gif_label = gif_label
        self.gif_path = gif_path
        self.frames = self.load_gif_frames()
        self.current_frame = 0
        self.play_gif()

    def load_gif_frames(self):
        gif = Image.open(self.gif_path)
        return [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif)]

    def play_gif(self):
        self.gif_label.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.gif_label.after(100, self.play_gif)  # Adjust delay as needed


class LearningGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Learning Game")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        
        self.speech_engine = SpeechEngine()
        self.current_gif = None
        self.current_index = 0
        self.best_times = {}  # Store best times for each word
        
        self.content = [
            {
                "gif": "g.png",
                "text": "This is a ball",
                "prompt": "Can you say 'ball'?",
                "target_word": "ball",
                "encouragements": [
                    "You can do it! Try saying 'ball' again.",
                    "Let's practice together. Listen carefully: 'ball'.",
                    "Take your time, you're doing great!",
                    "Almost there! Let's try one more time."
                ]
            },
            # Add more content items with similar structure
        ]
        
        self._create_ui()

    def _create_ui(self):
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(expand=True, fill="both", pady=20)
        
        self.gif_label = tk.Label(self.content_frame, bg="white")
        self.gif_label.pack(expand=True)
        
        self.text_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 20),
            bg="white",
            wraplength=700
        )
        self.text_label.pack(pady=20)
        
        self.timer_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 16),
            bg="white"
        )
        self.timer_label.pack(pady=5)
        
        self.best_time_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 14),
            bg="white"
        )
        self.best_time_label.pack(pady=5)
        
        self.status_label = tk.Label(
            self.content_frame,
            text="",
            font=("Arial", 16),
            bg="white"
        )
        self.status_label.pack(pady=10)
        
        self.button_frame = tk.Frame(self.root, bg="white")
        self.button_frame.pack(fill="x", pady=10)
        
        self.prev_button = tk.Button(
            self.button_frame,
            text="Previous",
            command=self._prev_item,
            font=("Arial", 14),
            bg="blue",
            fg="white",
            state="disabled"
        )
        self.prev_button.pack(side="left", padx=20)
        
        self.next_button = tk.Button(
            self.button_frame,
            text="Next",
            command=self._next_item,
            font=("Arial", 14),
            bg="green",
            fg="white",
            state="disabled"
        )
        self.next_button.pack(side="right", padx=20)

    def _update_timer_display(self, time_remaining):
        self.timer_label.config(text=f"Time remaining: {time_remaining:.1f}s")
        if time_remaining > 0:
            self.root.after(100, lambda: self._update_timer_display(time_remaining - 0.1))

    def _start_interaction(self):
        item = self.content[self.current_index]
        target_word = item["target_word"]
        
        def interaction_thread():
            self.prev_button.config(state="disabled")
            self.next_button.config(state="disabled")
            
            if target_word in self.best_times:
                self.best_time_label.config(
                    text=f"Best time: {self.best_times[target_word]:.1f}s"
                )
            
            self.speech_engine.speak(item["text"])
            time.sleep(1)
            self.speech_engine.speak(item["prompt"])
            
            self._update_timer_display(40.0)
            
            self.status_label.config(text="Listening...")
            response, time_taken = self.speech_engine.listen_with_timeout()
            
            if response and target_word in response:
                if time_taken < 40:
                    if target_word not in self.best_times or time_taken < self.best_times[target_word]:
                        self.best_times[target_word] = time_taken
                        self.best_time_label.config(
                            text=f"New best time: {time_taken:.1f}s!"
                        )
                    
                    self.status_label.config(text=f"Great job! Time: {time_taken:.1f}s")
                    self.speech_engine.speak("Excellent! Let's move to the next word!")
                    self.next_button.config(state="normal")
                    self.root.after(2000, self._next_item)
                else:
                    self.status_label.config(text="Good, but let's try to say it faster!")
                    self.speech_engine.speak("Good job! Let's try again, but a little faster this time!")
                    self.root.after(2000, self._start_interaction)
            else:
                encouragement = np.random.choice(item["encouragements"])
                self.status_label.config(text="Not quite. Let's try again!")
                self.speech_engine.speak(encouragement)
                self.root.after(2000, self._start_interaction)

        threading.Thread(target=interaction_thread).start()

    def _prev_item(self):
        self.current_index -= 1
        if self.current_index == 0:
            self.prev_button.config(state="disabled")
        self.next_button.config(state="disabled")
        self._load_item()

    def _next_item(self):
        self.current_index += 1
        if self.current_index == len(self.content) - 1:
            self.next_button.config(state="disabled")
        self.prev_button.config(state="normal")
        self._load_item()

    def _load_item(self):
        item = self.content[self.current_index]
        
        self.status_label.config(text="")
        self.timer_label.config(text="")
        self.best_time_label.config(text="")
        
        self.text_label.config(text=item["text"])
        self.current_gif = GifPlayer(self.gif_label, item["gif"])
        
        self.root.after(2000, self._start_interaction)

    def start_game(self):
        self._load_item()

if __name__ == "__main__":
    root = tk.Tk()
    game = LearningGame(root)
    game.start_game()
    root.mainloop()
