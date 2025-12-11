"""Speech to text module"""

import speech_recognition as sr
import sounddevice as sd
import soundfile as sf

def get_microphone_audio():
    """Function for converting microphone input to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            with open("ReadFile.txt", "w") as f:
                f.write(text)
        except sr.UnknownValueError:
            print("Failed to recognize audio")
        except sr.RequestError:
            print("Request Error")

def audio_file_to_text():
    """Function for converting an audiofile input to text"""
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile("Audio.wav")
    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            with open("ReadFile.txt", "w") as f:
                f.write(text)
        except sr.UnknownValueError:
                print("Failed to recognize audio")
        except sr.RequestError:
            print("Request Error")

def record_audio():
    """Function for recording device audio"""
    duration = 5
    fs = 48000

    device_index = 6

    device_info = sd.query_devices(device_index)
    devices = sd.query_devices()
    print(devices)
    print(device_info)

    channels = sd.query_devices(device=device_index, kind="output")['max_input_channels']

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels,
    dtype='float32', device=device_index)
    sd.wait()
    sf.write("Audio.wav", recording, fs)
