import math
import numpy as np
import random

# This function initialize weight vector for each digit class with random number of weights.

def init_weight(bias):
    class_weight = [0]*10
    for i in range(10):
        if bias:
            class_weight[i] = np.random.rand(28 * 28+1)
        else:
            class_weight[i] = np.random.rand(28*28)
    return class_weight

# func: This function receives the name of image file and label file as input.
#       Then it will read through both files and record the probability in a local NumClass array.
#       In the end, it will return the NumClass array

def readTrainingFiles(imageFileName, labelFileName, weight_class, bias):
    imageFile = open(imageFileName, 'r')
    labelFile = open(labelFileName, 'r')
    # Create a NumClass array
    arr_NumClass = []
    correct = 0
    count = 0
    training_data = []
    label_data = []
    label_count = 0
    while True:
        currLabel = labelFile.read(1)
        if currLabel == '\n':
            currLabel = labelFile.read(1)
        # Using currLabel to determine when we finish reading the training files
        if not currLabel:
            break
        currLabel = int(currLabel)
        #
        if bias:
            cur_digit = np.zeros(28*28+1)
        else:
            cur_digit = np.zeros(28*28)
        for x in range(28*28):

                cell = imageFile.read(1)
                if cell == '\n':
                    cell = imageFile.read(1)
                #
                feature = 0
                if cell != ' ':
                    feature = 1
                cur_digit[x] = feature
        if bias:
            cur_digit[27*27+1] = 1
        label_data.append(currLabel)
        training_data.append(cur_digit)
        label_count += 1
    epoch = 60
    for e in range(epoch):
        a = 80/(80+e)
        guess = np.zeros(10)
        #random ordering
        itrange = list(range(label_count))
        random.shuffle(itrange)
        wrong = 0
        for x in itrange:
            for i in range(10):
                guess[i] = np.dot(weight_class[i], training_data[x])
            guess_label = np.argmax(guess)
            # training begin if wrong classfication:
            if guess_label != label_data[x]:
                weight_class[label_data[x]] = weight_class[label_data[x]] + a*training_data[x]
                weight_class[guess_label] = weight_class[guess_label] - a*training_data[x]
                wrong += 1
        print(wrong/label_count )
        # training complete
    return weight_class


def readTestFiles(imageFileName, labelFileName, weight_class, bias):
    imageFile = open(imageFileName, 'r')
    labelFile = open(labelFileName, 'r')
    # Create a NumClass array
    training_data = []
    label_data = []
    label_count = 0
    while True:
        currLabel = labelFile.read(1)
        if currLabel == '\n':
            currLabel = labelFile.read(1)
        # Using currLabel to determine when we finish reading the training files
        if not currLabel:
            break
        currLabel = int(currLabel)
        #
        if bias:
            cur_digit = np.zeros(28 * 28+1)
        else:
            cur_digit = np.zeros( 28*28)
        for x in range(28*28):
                cell = imageFile.read(1)
                if cell == '\n':
                    cell = imageFile.read(1)
                #
                feature = 0
                if cell != ' ':
                    feature = 1
                cur_digit[x] = feature
        if bias:
            cur_digit[27*27+1] = 1

        label_data.append(currLabel)
        training_data.append(cur_digit)
        label_count += 1
    correct = 0
    for x in range(label_count):
        guess = np.zeros(10)
        for i in range(10):
            guess[i] = np.dot(weight_class[i], training_data[x])
        guess_label = np.argmax(guess)
        # training begin if wrong classfication:
        if guess_label == label_data[x]:
            correct += 1
        # training complete
    print(correct/label_count)
def print_image(test_imageFileName, test_labelFileName, imageNum):
    imageFile = open(test_imageFileName, 'r')
    labelFile = open(test_labelFileName, 'r')
    counter = 1
    while True:
        currLabel = labelFile.read(1)
        if currLabel == '\n':
            currLabel = labelFile.read(1)
        # Using currLabel to determine when we finish reading the training files
        if not currLabel:
            break
        #
        if counter == imageNum:
            for i in range(28):
                string =imageFile.readline()
                print(string[0:len(string)-1],'|')

        else:
            for i in range(28):
                string = imageFile.readline()
        counter += 1




bias = 1

class_weight = init_weight(bias)
test = readTrainingFiles('digitdata/trainingimages','digitdata/traininglabels', class_weight, bias)
# calculate_probability(test)
readTestFiles('digitdata/testimages', 'digitdata/testlabels', test,bias )

# print_ratio(test[8])

# numPair = [(test[4], test[9]), (test[5], test[3]), (test[7], test[9]), (test[8], test[3])]
# odd_ratio(numPair)
