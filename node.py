import datetime
import voice
import os
import wikipedia
import string
from Dependencies import search

dt = datetime.datetime.now()
td = datetime.timedelta


def change_presets():
    while True:
        voice.speak("Which setting would you like to change?")
        key = voice.takeCommand()
        with open("Dependencies/Presets.txt", "r") as file:
            data = file.read()
            try:
                index = data.index(key) + len(key) + 1
                break
            except:
                continue
    voice.speak("What would you like the new value to be?")
    value = voice.takeCommand()
    end_index = data[index:].index("$")
    with open("Dependencies/Presets.txt", "w") as file:
        file.write(data[:index] + value + data[index + end_index :])
    return "Changes saved"


def open_app(partial_address):
    voice.speak("Opening it now " + voice.title)
    address = os.getenv("DESK_PATH") + partial_address
    os.system(address)
    return "App closed"


def spec_fic_search():
    voice.speak("What would you like to search for " + voice.title)
    return search.search(voice.takeCommand())


def get_time(format):
    return dt.strftime(format)


def get_date(delta):
    delta = int(delta)
    return (dt + td(delta)).strftime("%m-%d-%Y")


def search_mode():
    while True:
        voice.speak("What would you like to search for?")
        voice.speak(wikipedia.summary(voice.takeCommand(), sentences=3))
        voice.speak("Would you like to continue searching " + voice.title + "?")
        response = voice.takeCommand()
        if "no" in response or "exit" in response:
            break
    return "Finished search"


def change_directory():
    voice.speak("Which directory would you like to enter?")
    address = voice.takeCommand()
    address = string.capwords(address)
    address = address.replace(" / ", "/")
    address = address.replace(" Slash ", "/")
    path = os.getenv("DESK_PATH") + address
    try:
        os.chdir(path)
        return "Successfully navigated to directory"
    except:
        return "No such directory can be located"


def open_file():
    voice.speak("What is the file name " + voice.title + "?")
    file = voice.takeCommand()
    file = file.replace(" ", ".")
    try:
        os.system("open " + file)
        return "Opened " + file
    except:
        return "No such file found"


def get_news():
    return search.getNews()


def get_weather():
    return search.getWeather()


class Node:
    def __init__(self, words, response, connections=[]):
        self.words = words
        self.response = response
        self.connections = connections

    def get_response(self):
        try:
            func_name = self.response.split("{")
            call = globals()[func_name[0]]
            param = func_name[1][:-1]
            return call(param) if param != "" else call()
        except:
            return self.response

    def get_words(self):
        return self.words

    def get_connections(self):
        cd = {}
        for x in self.connections:
            cd[x.get_words()] = x
        return cd
