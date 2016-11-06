import math

def open_training_set():
    with open("rt-train.txt")as f:
        train = f.read().splitlines()
    return train

def naive_bayes_training(train):
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
                sum1 += 1
        else:               #negative review
            ncount +=1
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in d2v:
                    d2v[temp[0]] = 0
                d2v[temp[0]] += int(temp[1])
                sum2 += 1
    for key, value in d1v.items():
        d1v[key] = math.log(d1v[key]/sum1)
    for key, value in d2v.items():
        d2v[key] = math.log(d2v[key]/sum2)
    pp = (pcount)/(pcount+ncount)
    return d1v, d2v, pp


def evaluation(d1v, d2v, pp):
    with open("rt-test.txt")as f:
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
            if temp[0] in d1v and temp[0] in d2v:
                psum += d1v[temp[0]]*int(temp[1])
                nsum += d2v[temp[0]]*int(temp[1])
        lp = math.log(pp) + psum
        ln = math.log(1-pp) + nsum
        if lp>ln and result == '1':
            correct += 1
        elif lp>ln and result == '-1':
            correct += 1
        elif lp<=ln and result == '1':
            wrong += 1
        elif lp<=ln and result =='-1':
            wrong += 1
    accuracy = correct/(correct+wrong)
    return accuracy




train = open_training_set()
vocab1, vocab2, pp = naive_bayes_training(train)
print(pp)
print(evaluation(vocab1, vocab2, pp))
