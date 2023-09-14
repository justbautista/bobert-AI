import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import json
import random
import pickle
import colorama
from colorama import Fore, Style
import sys
import os
import fnmatch
from pathlib import Path
import re
from datetime import date, timedelta
import requests
import geocoder
import json
from dotenv import load_dotenv

load_dotenv()

def correct(prevInput, currInput, jsonFile):
    currInputArray = currInput.split()
    newTag = currInputArray[-1]
    foundTag = False
    output = ""

    try:
        with open(jsonFile, "r") as file:
            data = json.load(file)
    except:
        return "JSON file was not found"

    for intent in data["intents"]:
        if intent["tag"] == newTag:
            intent["patterns"].append(prevInput)
            foundTag = True
            break

    if foundTag:
        with open(jsonFile, "w") as file:
            json.dump(data, file)
            output = f"Okay, I will remember that, '{prevInput}', is a {newTag}"
    else:
        output = f"'{newTag}' tag doesn't exist"

    return output


##################################################

API_KEY = os.environ["API_KEY"]
DAY_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
CURRENT_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "imperial"

loc = geocoder.ip("me").latlng


def createUrl(baseUrl):
    url = f"{baseUrl}lat={loc[0]}&lon={loc[1]}&units={UNITS}&appid={API_KEY}"
    return url


def findDayWeather(day):
    url = createUrl(DAY_BASE_URL)
    response = requests.get(url).json()

    if day == "today":
        theDay = str(date.today())
    else:
        theDay = str(date.today() + timedelta(days=1))

    hi = -300
    lo = 300
    hiWind = -10000
    loWind = 10000
    descriptions = set()
    theDayFound = False
    output = ""
    city = response["city"]["name"]
    country = response["city"]["country"]

    for i in range(response["cnt"]):
        dateFormatted = response["list"][i]["dt_txt"].split()[0]
        hiTemp = response["list"][i]["main"]["temp_max"]
        loTemp = response["list"][i]["main"]["temp_min"]
        description = response["list"][i]["weather"][0]["description"]
        windSpeed = response["list"][i]["wind"]["speed"]

        if dateFormatted == theDay:
            hi = max(hiTemp, hi)
            lo = min(loTemp, lo)
            hiWind = max(windSpeed, hiWind)
            loWind = min(windSpeed, loWind)
            descriptions.add(description)
            theDayFound = True

    if theDayFound:
        if day == "today":
            output = f"\n\n\tRest of Day\n"
        else:
            output = f"\nWeather Summary For Tomorrow in {city}, {country}:\n\n"

        output += f"\tTemperature Range(Fahrenheit): {lo} - {hi}\n"
        output += f"\tWind Speed Range(mph): {loWind} - {hiWind}\n"
        output += "\tDescription: "

        for i, desc in enumerate(descriptions):
            if i == len(descriptions) - 1:
                output += desc
                break

            output += f"{desc}, "

    output += "\n"
    return output


def findCurrentWeather():
    url = createUrl(CURRENT_BASE_URL)
    response = requests.get(url).json()

    city = response["name"]
    country = response["sys"]["country"]
    temperature = response["main"]["temp"]
    wind = response["wind"]["speed"]
    description = response["weather"][0]["description"]

    output = f"\nWeather Summary For Today in {city}, {country}:\n\n"
    output += "\tCurrent\n"
    output += f"\tTemperature(Fahrenheit): {temperature}\n"
    output += f"\tWind Speed(mph): {wind}\n"
    output += f"\tDescription: {description}"

    return output


def findWeatherToday():
    return findCurrentWeather() + findDayWeather("today")


######################################################


def find(pattern, path):
    if "." not in pattern:
        newPattern = f"*{pattern}*"
    else:
        newPattern = pattern

    newPath = str(Path.home()) + path

    resultFiles = []
    resultDirs = []
    for root, dirs, files in os.walk(newPath):
        for name in files:
            if fnmatch.fnmatch(name, newPattern):
                resultFiles.append(os.path.join(root, name))

        for name in dirs:
            if fnmatch.fnmatch(name, newPattern):
                resultDirs.append(os.path.join(root, name))

    return formatOutput(resultFiles, resultDirs)


def formatOutput(files, dirs):
    output = "\n\nThis is what I found:\n\n"

    if len(files) != 0:
        output += "Files:\n"

        for file in files:
            output += f"\t{file}\n"

    if len(dirs) != 0:
        output += "Directories:\n"

        for dir in dirs:
            output += f"\t{dir}\n"

    return output


def stripInput(input):
    inList = input.split()
    commonPreFind = ["find", "for", "search", "is"]

    if (
        len(re.findall("^.*\..*$", inList[-1])) == 0
        or inList[-2].lower() in commonPreFind
        or (len(inList) == 0 and len(re.findall("^.*\..*$", inList[-1])) == 0)
    ):
        return inList[-1]

    for i in range(len(inList))[:0:-1]:
        if (
            len(re.findall("^.*\..*$", inList[i])) == 0
            or inList[i - 1].lower() in commonPreFind
        ):
            return inList[i]


def trainWeather():
    return


###########################################################

nltk.download("punkt")
colorama.init()
stemmer = LancasterStemmer()

# easier way to retrain model
if "--train" in sys.argv[1:]:
    TRAIN = True

    for filename in os.listdir():
        if (
            "model_bobert" in filename
            or "checkpoint" in filename
            or "data.pickle" in filename
        ):
            os.remove(filename)
else:
    TRAIN = False

# preprocessing data
with open("intents.json") as file:
    data = json.load(file)

if TRAIN:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w not in ",?!.:;"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
else:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

# model creation
tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# model training
if TRAIN:
    model.fit(training, output, n_epoch=200, batch_size=8, show_metric=True)
    model.save("model_bobert")
else:
    model.load("model_bobert")


# preprocessor for user input
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


# chat
def chat():
    os.system("clear")
    print("Start talking... (type quit to stop)")
    messageArray = []

    while True:
        rand = False
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()

        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.7:
            for tg in data["intents"]:
                if tg["tag"] == tag:
                    if tag == "filesearch":
                        fileOrDir = stripInput(inp)
                        responses = find(fileOrDir, "/")
                    elif tag == "weathertoday":
                        responses = findWeatherToday()
                    elif tag == "weathertomorrow":
                        responses = findDayWeather("tomorrow")
                    elif tag == "correction":
                        if len(messageArray) == 0:
                            responses = "There is no previous message to correct"
                        else:
                            responses = correct(messageArray[-1], inp, "intents.json")
                    else:
                        responses = tg["responses"]
                        rand = True

            if rand:
                responses = random.choice(responses)

            print(Fore.GREEN + "Bobert:" + Style.RESET_ALL, responses)
        else:
            print(Fore.GREEN + "Bobert:" + Style.RESET_ALL, "Sorry, I don't understand")

        messageArray.append(inp)


chat()
