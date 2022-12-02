# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 21:32:39 2022

@author: neveen
Program that is the main file in which the Chatbot model will work from
and respond to inputs given.
"""

# required modules
import json
import pickle
import random
import nltk
import numpy as np
from keras.models import load_model
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()

# loading the files we made previously
intents = json.loads(open("intents.json", encoding="utf8").read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

# This function will separate words from the sentences we’ll give as input.


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# This function will append 1 to a list variable ‘bag’ if the word is
#  contained inside our input and is also present in the list of words
#  created earlier.


def bag_of_words(sentence):

    # separate out ‘root’ words from the input sentence
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)

    # check whether the word in the input is also in the words list.
    # If it is, we’ll append 1 to the bag, otherwise it’ll remain 0
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    # Return a numpy array of the list variable bag that now contains 1’s and 0’s.
    return np.array(bag)

# This function will predict the class of the sentence input by the user.
# Initialize a variable bow that will contain a NumPy array of 0’s and 1’s,
# using the function defined above. Using the predict() function,
# we’ll predict the result based on the user’s input.
# Initialize a variable ERROR_THRESHOLD and append from ‘res’ if the value
# is greater than the ERROR_THRESHOLD, then sort it using the sort function.


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    # store the tag or classes that was in the intents.json file.
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# This function will print a random response from whichever class
# the sentence/words input by the user belongs to.
# If the tag matches the tags in the list_of_intents, store a
# random response in a variable called result,
# using the choice() method of the random module.


bot_name = "Codee"


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])  # prints a random response


'''def bot_greeting(text):

    greeting = "I am Codee the chatbot and I can assist with your computer science FAQS! Ask away😀.Type quit to leave this session at anytime"
    print(greeting)'''


def chatbot_response(text):
    ints = predict_class(text)
    res = get_response(ints, intents)
    return res


# prompt the user for an input and print the Chatbot’s response.
#print("I am Codee the chatbot and I can assist with your computer science FAQS! Ask away😀.Type quit to leave this session at anytime")
'''while True:
    message = input("")
    if message == "quit":
        break'''
