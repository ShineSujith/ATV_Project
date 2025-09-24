"""Main application module"""

import speech_recognition as sr

recognizer = sr.Recognizer()

def get_microphone_audio():
    """Function for converting microphone input to text"""
    with sr.Microphone() as source:
        audio = recognizer.listen(source, duration=5)
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Failed to recognize audio")
        print(text)

get_microphone_audio()
