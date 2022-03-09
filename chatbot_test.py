
import random
import json
import pickle
import numpy as np
import os
import sys

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

intents = json.loads(open(r'C:\Users\ASUS\PycharmProjects\pythonProject3\intents.json').read())
lemmatizer = WordNetLemmatizer()

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


def _clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def _bag_of_words(sentence, words):
    sentence_words = _clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)


def _predict_class(sentence):
    p = _bag_of_words(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.15
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    return return_list

def _get_response(ints, intents_json):
    try:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag']  == tag:
                result = random.choice(i['responses'])
                break
    except IndexError:
        result = "I don't understand!"

    return result

print("Go! bot is running")

while True :
    message= input("")
    ints = _predict_class(message)
    res = _get_response(ints,intents)
    print(res)
