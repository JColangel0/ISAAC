import pyttsx3
import speech_recognition as sr


def read_data(key, data):
    index = data.index(key) + len(key)
    value = data[index : index + data[index:].index("$")]
    return value


with open("Dependencies/Presets.txt", "r") as f:
    content = f.read()
    title = read_data("title:", content)
    rate = read_data("speed:", content)
    timeout = float(read_data("delay:", content))
    phrase_limit = float(read_data("limit:", content))

engine = pyttsx3.init("nsss")
voices = engine.getProperty("voices")  # 24, 14
engine.setProperty("voice", voices[14].id)
engine.setProperty("rate", rate)


def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening")
                audio = r.listen(source, timeout, phrase_limit)
                Query = r.recognize_google(audio, language="en-us")
                print(Query)
                break
            except Exception as e:
                print(e)
                speak("Say that again")
        return Query.lower()
