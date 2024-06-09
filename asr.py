import pvporcupine
import pyaudio
import numpy as np
from transformers import pipeline
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Picovoice access key
access_key = os.getenv("PICOVOICE_API_KEY")
if not access_key:
    raise ValueError("Access key not found. Make sure to set it in the .env file.")

# Initialize Porcupine for "Jarvis" and "terminator" hotwords
keywords = ["jarvis", "terminator"]
porcupine = pvporcupine.create(access_key=access_key, keywords=keywords)
pa = pyaudio.PyAudio()

# Set up the audio stream
audio_stream = pa.open(
    rate=porcupine.sample_rate,  # Typically 16000 Hz
    channels=1,                  # Mono
    format=pyaudio.paInt16,      # 16-bit PCM
    input=True,
    frames_per_buffer=porcupine.frame_length
)

# Initialize the speech-to-text model with language set to English
speech_to_text = pipeline("automatic-speech-recognition", model="openai/whisper-base")

def listen_for_commands():
    print("Listening for 'Jarvis' or 'terminator' hotwords...")
    while True:
        try:
            # Read PCM audio data from the stream
            pcm_data = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_data = np.frombuffer(pcm_data, dtype=np.int16)

            # Check if a keyword is detected
            keyword_index = porcupine.process(pcm_data)
            if keyword_index >= 0:
                detected_keyword = keywords[keyword_index]
                print(f"Hotword Detected: '{detected_keyword}'")

                if detected_keyword == "jarvis":
                    handle_jarvis_command()
                elif detected_keyword == "terminator":
                    print("Termination command received. Exiting...")
                    break  # Exit the loop to terminate the process
            else:
                print("No hotword detected, continuing to listen...")

        except Exception as e:
            print(f"Error in listening loop: {e}")
            break  # Exit the loop in case of error

def handle_jarvis_command():
    # Capture audio for the command (next 5 seconds)
    print("Listening for command...")
    command_audio_data = []
    for _ in range(int(porcupine.sample_rate / porcupine.frame_length * 5)):  # 5 seconds of audio
        pcm_data = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_data = np.frombuffer(pcm_data, dtype=np.int16)
        command_audio_data.append(pcm_data)
    
    # Convert the captured command audio data to a single NumPy array
    command_pcm_data = np.concatenate(command_audio_data)
    
    # Transcribe PCM audio to text using Whisper model
    result = speech_to_text(command_pcm_data)
    transcription = result['text']
    print(f"Transcribed Command: {transcription}")

    # You can process the command if needed
    # For example: process_command(transcription)

def process_command(command):
    # Example function to process the transcribed command
    print(f"Processing command: {command}")

# Start listening for commands
try:
    listen_for_commands()
finally:
    # Cleanup resources
    if audio_stream.is_active():
        audio_stream.stop_stream()
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
