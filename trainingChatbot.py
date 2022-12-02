# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 21:29:48 2022

@author: neveen
This program is to train our chatbot model to recognize phrases and patterns.
When this program runs, it'll output 200 epochs.
Epochs indicate the number of passes of the entire training
dataset the machine learning algorithm has completed.
"""
import numpy as np
import nltk #leading platform for building Python programs to work with human language data.
import random
import json
import pickle  # To save data into files

from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

#class called WordNetLemmatizer() which will give the root words of the words
#that the Chatbot can recognize. For example, for hunting, hunter, hunts
#and hunted, the lemmatize function of the WordNetLemmatizer() class will 
#give “hunt” because it is the root word.
lemmatizer = WordNetLemmatizer()

#Read the contents from the “intense.json” file and store it to a variable “intents”
intents = json.loads(open("intents.json", encoding="utf8").read())

# initialize empty lists to store the contents
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

#function word_tokenize() takes a sentence as a parameter and
#then returns a list containing all the words of the sentence as strings.
#Here we’re tokenizing the patterns and then appending them to a list ‘words’. 
#So, at last, this list ‘words’ would have all the words that are in the ‘patterns’ list.
#In documents, we have all the patterns with their tags in the form of a tuple.
#using a list comprehension, we’ll modify the list ‘words’ we created and store
#the words’ ‘lemma’  or simply put, the root words. 
#Dump the data of the ‘words’ and ‘classes’ to binary files of the same name, 
#using the pickle module’s dump() function.
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # separating words from patterns
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list) # and adding them to words list

        # associating patterns with respective tags
        documents.append((word_list, intent['tag']))

        # appending the tags to the class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# storing the root words or lemma
words = [lemmatizer.lemmatize(word)
         for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# saving the words and classes list to binary files
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))


#classify our data into 0’s and 1’s because neural networks
# works with numerical values, not strings or anything else.
#Create an empty list called training, in which we’ll store the data used for training.
#output_empty list will store as many 0’s as there are classes in the intents.json file
training = []
output_empty = [0] * len(classes)

#create a bag that will store the 0’s and 1’s. (0, if the word isn’t in the pattern
# and 1 if the word is in the pattern). To do that, we’ll iterate through the
# documents list and append 1 to the ‘bag’ if it is  not in the patterns, 0 otherwise.
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(
        word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

     # making a copy of the output_empty
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

#shuffle this training set and make it a numpy array.
random.shuffle(training)
training = np.array(training)

# Split the training set consisting of 1’s and 0’s into two parts, 
# that is train_x and train_y. 
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# creating a Sequential machine learning model
# that will train on the dataset prepared above.
#Add():  This function is used to add layers in a neural network.
#Dropout(): This function is used to avoid overfitting
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# compiling the model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=200, batch_size=5, verbose=1)
 # an H5 file is used to store large amount of data in the form of multidimensional arrays.
 #  The format is primarily used to store scientific data that is well-organized
 #  for quick retrieval and analysis
model.save('chatbotmodel.h5', hist) # saving the model
print("Done") # shows successful training of the Chatbot model

