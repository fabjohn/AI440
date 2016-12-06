import math
import numpy as np
import random
import operator
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

def read_Files(imageFileName, labelFileName, bias):
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
            cur_digit[28*28] = 1
        label_data.append(currLabel)
        training_data.append(cur_digit)
        label_count += 1
    return label_data, training_data

def perceptron_training(training_data, label_data, weight_class):
    epoch = 150
    label_count = len(label_data)
    for e in range(epoch):
        a = 100/(100+e)
        guess = np.zeros(10)
        # random ordering
        itrange = list(range(label_count))
        random.shuffle(itrange)
        wrong = 0
        for x in itrange:
            for i in range(10):
                guess[i] = np.dot(weight_class[i], training_data[x])
            guess_label = np.argmax(guess)
            # training begin if wrong classfication:
            if guess_label != label_data[x]:
            #attempt for implemeting differentiable perceptron
                dotp = np.dot(weight_class[label_data[x]], training_data[x])
                sigmoid1 = 1/(1+np.exp(-dotp))
                dotn = np.dot(weight_class[guess_label], training_data[x])
                sigmoid2 = 1/(1+np.exp(-dotn))
                weight_class[label_data[x]] = weight_class[label_data[x]] + a*training_data[x]#*sigmoid1* (1-sigmoid1)
                weight_class[guess_label] = weight_class[guess_label] - a*training_data[x]#*sigmoid2 *(1-sigmoid1)
                wrong +=1
           #print(label_data[x], guess_label)
        print(1-wrong/label_count)
        # training complete
    return weight_class


def perceptron_classfication(testing_data, label_data, weight_class):
    correct = 0
    label_count = len(label_data)
    cm = []
    for i in range(10):
        temp = [0]*10
        cm.append(temp)
    single_digit_count = [0]*10
    for x in range(label_count):
        guess = np.zeros(10)
        for i in range(10):
            guess[i] = np.dot(weight_class[i], testing_data[x])
        guess_label = np.argmax(guess)
        # training begin if wrong classfication:
        if guess_label == label_data[x]:
            correct += 1
        # training complete
        single_digit_count[label_data[x]] += 1
        cm[label_data[x]][guess_label] += 1
    for n in range(10):
        for m in range(10):
            cm[n][m] = cm[n][m]/single_digit_count[n]
    cmm = np.matrix(cm)
    print(correct/label_count)


# Part2.2 using Euclidean
def get_distance(test, train):
    distance = 0
    for x in range(28*28):
        distance += pow((test[x] - train[x]),2)
    return math.sqrt(distance)
#using hamming distance
def get_distance1(test, train):
    distance = 0
    for x in range(28*28):
        distance += abs(test[x]- train[x])
    return distance

def get_neighbors(test_data, train_data, train_label, k):
    distances = []
    for x in range(len(train_data)):
        #temp = np.count_nonzero(test_data!=train_data[x])
        temp = np.linalg.norm(test_data - train_data[x])
        # temp = get_distance1(test_data, train_data[x])
        distances.append((temp, train_label[x]))
    distances.sort(key=operator.itemgetter(0))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][1])       #append label
    return neighbors

def get_votes(neighbors):
    votes = {}
    for x in range(len(neighbors)):
        guess_label = neighbors[x]
        if guess_label in votes:
            votes[guess_label] += 1
        else:
            votes[guess_label] = 1
    sorted_votes = sorted(votes.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_votes[0][0]

def KNN_main(training_data, training_label, testing_data, testing_label, k):
    label_count = len(testing_label)
    correct = 0
    count = 0
    cm = []
    for i in range(10):
        temp = [0]*10
        cm.append(temp)
    single_digit_count = [0] * 10
    for x in range(label_count):
        neighbors = get_neighbors(testing_data[x], training_data, training_label, k)
        predict = get_votes(neighbors)
        if predict == testing_label[x]:
            correct += 1
        count +=1
        single_digit_count[testing_label[x]] += 1
        cm[testing_label[x]][predict] += 1
        print(correct/count)
    for n in range(10):
        for m in range(10):
            cm[n][m] = cm[n][m]/single_digit_count[n]
    print(cm)
    print(correct/label_count)



bias = 0
k = 4
perceptron = 1      #0 if you want to use knn
class_weight = init_weight(bias)
label, training = read_Files('digitdata/trainingimages','digitdata/traininglabels', bias)
# for n in range(10):
#     print(trained_weight[n].tolist())
test_label, testing_data = read_Files('digitdata/testimages', 'digitdata/testlabels', bias)
if perceptron == 1:
    trained_weight = perceptron_training(training, label, class_weight)
    perceptron_classfication(testing_data, test_label, trained_weight)
else:
    KNN_main(training, label, testing_data, test_label, k)
