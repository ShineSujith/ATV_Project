"""Speech to text module"""

import speech_recognition as sr

def get_microphone_audio(continue_recongition: bool):
    """Function for converting microphone input to text"""
    recognizer = sr.Recognizer()
    transcript = ""
    while continue_recongition:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                print(text)
                transcript = f"{transcript} {text}"
                user_input = input("Continue Transcribing (y/n)").lower()
                if user_input == "n":
                    continue_recongition = False
            except sr.UnknownValueError:
                print("Failed to recognize audio")
            except sr.RequestError:
                print("Request Error")
    print(transcript)
