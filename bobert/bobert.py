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

nltk.download('punkt')
colorama.init()
stemmer = LancasterStemmer()  

# easier way to retrain model
if "--train" in sys.argv[1:]:
    TRAIN = True

    for filename in os.listdir():
        if "model_bobert" in filename or "checkpoint" in filename or "data.pickle" in filename:
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
    model.fit(training, output, n_epoch=500, batch_size=8, show_metric=True)
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
    os.system('cls')
    print("Start talking... (type quit to stop)")

    while True:
        print(Fore.LIGHTBLUE_EX + "User: " + Style.RESET_ALL, end="")
        inp = input()

        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.8:
            for tg in data["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]

            print(Fore.GREEN + "Bobert:" + Style.RESET_ALL , random.choice(responses))
        else:
            print(Fore.GREEN + "Bobert:" + Style.RESET_ALL , "Sorry, I don't understand")

chat()
