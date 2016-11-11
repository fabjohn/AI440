import math

def open_training_set(data):
    if data == '1':
        with open("rt-train.txt")as f:
            train = f.read().splitlines()
    else:
        with open("fisher_train_2topic.txt")as f:
            train = f.read().splitlines()
    return train

def multi_nb_training(train):
    vocab = set([])
    d1v = {}        #positive dict
    d2v = {}        #negative dict
    sum1 = 0
    sum2 = 0
    pcount = 0
    ncount =0
    for row in train:
        currow = row.split(' ')
        if currow[0] == '1': #positve review
            pcount += 1
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in d1v:
                    d1v[temp[0]] = 0
                d1v[temp[0]] += int(temp[1])
                sum1 += int(temp[1])
        else:               #negative review
            ncount +=1
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in d2v:
                    d2v[temp[0]] = 0
                d2v[temp[0]] += int(temp[1])
                sum2 += int(temp[1])

    for key, value in d1v.items():
        if key not in d2v:
            d2v[key] = 0
    for key, value in d2v.items():
        if key not in d1v:
            d1v[key] = 0
    print(len(d1v))
    print(len(d2v))
    for key, value in d1v.items():
        d1v[key] = math.log((d1v[key]+1)/(sum1+len(d1v)))
    for key, value in d2v.items():
        d2v[key] = math.log((d2v[key]+1)/(sum2+len(d1v)))
    pp = (pcount)/(pcount+ncount)
    return d1v, d2v, pp

def bernoulli_nb(train):
    vocab = set([])
    d1v = {}        #positive dict
    d2v = {}        #negative dict
    sum1 = 0        #total positive reviews
    sum2 = 0        #total negative reviews
    pcount = 0
    ncount =0
    for row in train:
        currow = row.split(' ')
        if currow[0] == '1': #positve review
            pcount += 1
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in d1v:
                    d1v[temp[0]] = 0
                d1v[temp[0]] += 1       #wordcount doesn't matter
            #sum1 += 1       #count one positve review
        else:               #negative review
            ncount +=1
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in d2v:
                    d2v[temp[0]] = 0
                d2v[temp[0]] += 1
            #sum2 += 1
    for key, value in d1v.items():
        if key not in d2v:
            d2v[key] = 0
    for key, value in d2v.items():
        if key not in d1v:
            d1v[key] = 0
    v = len(d1v)
    for key, value in d1v.items():
        d1v[key] = math.log((d1v[key]+1)/(pcount+v))
    for key, value in d2v.items():
        d2v[key] = math.log((d2v[key]+1)/(ncount+v))
    pp = (pcount)/(pcount+ncount)
    return d1v, d2v, pp


def evaluation(d1v, d2v, pp, data):
    if data == '1':
        with open("rt-test.txt")as f:
            test = f.read().splitlines()
    else:
        with open("fisher_test_2topic.txt")as f:
            test = f.read().splitlines()
    correct = 0
    wrong = 0
    for row in test:
        currow = row.split(' ')
        result = currow[0]
        del currow[0]
        psum = 0
        nsum = 0
        for word in currow:
            temp = word.split(':')
            if temp[0] in d1v:
                psum += d1v[temp[0]]*int(temp[1])
                nsum += d2v[temp[0]]*int(temp[1])
                #psum += d1v[temp[0]]*int(temp[1])
                #nsum += d2v[temp[0]]*int(temp[1])
        lp = math.log(pp) + psum
        ln = math.log(1-pp) + nsum
        if lp>ln and result == '1':
            correct += 1
        elif lp>ln and result == '-1':
            wrong += 1
        elif lp<=ln and result == '1':
            wrong += 1
        elif lp<=ln and result =='-1':
            correct += 1
    accuracy = correct/(correct+wrong)
    return accuracy



type = input('enter the model you want to use:(1 is Multinomial, 2 is Bernoulli)')
data = input('enter the corpora you wnat to review:(1 is Movie, 2 is Convo topic)')

train = open_training_set(data)
if type == '1':
    vocab1, vocab2, pp = multi_nb_training(train)
else:
    vocab1, vocab2, pp = bernoulli_nb(train)
print(evaluation(vocab1, vocab2, pp, data))
