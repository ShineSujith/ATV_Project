import speech_recogniton as sr

recognizer = sr.Recoginizer()

def getMicrophoneAudio():
    with recognizer.Microphone() as source:
        audio = recognizer.listen(source, duration=5)
        try:
            text = recognizer.recognize_google(audio)
        except:
            print("An Error has occured")
        print(text)

getMicrophoneAudio()
