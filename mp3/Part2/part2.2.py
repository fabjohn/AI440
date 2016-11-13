import math

def open_training_set():
    with open("fisher_train_40topic.txt")as f:
        train = f.read().splitlines()
    return train

def multi_nb_training(train):
    d1v = {}        #positive dict
    d2v = {}        #negative dict
    sum1 = 0
    sum2 = 0
    pcount = 0
    ncount =0
    dict_list = [0]*40
    count_list = [0]*40
    for row in train:
        currow = row.split(' ')
        topic = int(currow[0])
        if dict_list[topic] == 0:
            cur_dict = {}
            count_list[topic] += 1
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in cur_dict:
                    cur_dict[temp[0]] = 0
                cur_dict[temp[0]] += int(temp[1])
                sum1 += int(temp[1])
            dict_list[topic] = cur_dict
        else:               #negative review
            count_list[topic] += 1
            cur_dict = dict_list[topic]
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in cur_dict:
                    cur_dict[temp[0]] = 0
                cur_dict[temp[0]] += int(temp[1])
                sum2 += int(temp[1])
            dict_list[topic] = cur_dict
    for topic in dict_list:

    for key in d1v:
        if key not in d2v:
            d2v[key] = 0
    for key in d2v:
        if key not in d1v:
            d1v[key] = 0
    for key in d1v:
        d1v[key] = math.log((d1v[key]+1)/(sum1+len(d1v)))
    for key in d2v:
        d2v[key] = math.log((d2v[key]+1)/(sum2+len(d1v)))
    pp = (pcount)/(pcount+ncount)
    return d1v, d2v, pp

def bernoulli_nb(train):
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
    for key in d1v:
        if key not in d2v:
            d2v[key] = 0
    for key in d2v:
        if key not in d1v:
            d1v[key] = 0
    # v = len(d1v)
    # for key, value in d1v.items():
    #     d1v[key] = math.log((d1v[key]+1)/(pcount+v))
    # for key, value in d2v.items():
    #     d2v[key] = math.log((d2v[key]+1)/(ncount+v))
    v = len(d1v)
    for key in d1v:
        d1v[key] = [math.log((d1v[key]+1)/(pcount+v)),math.log((pcount-d1v[key]+1)/(pcount+v))]
    for key in d2v:
        d2v[key] = [math.log((d2v[key]+1)/(ncount+v)),math.log((ncount-d2v[key]+1)/(ncount+v))]
    pp = (pcount)/(pcount+ncount)
    return d1v, d2v, pp


def m_testing(d1v, d2v, pp, data):
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


def b_testing(d1v, d2v, pp, data):
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
        doc_word = []
        for word in currow:
            temp = word.split(':')
            if temp[0] in d1v:
                doc_word.append(temp[0])       #only append when word in the dictionary

        for vocab in d1v:
            pos_word = d1v[vocab]
            neg_word = d2v[vocab]
            if vocab in doc_word:           #if the dictionary word occurs at current document
                psum += pos_word[0]
                nsum += neg_word[0]
            else:
                psum += pos_word[1]
                nsum += neg_word[1]
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
if type == '1':
    print(m_testing(vocab1, vocab2, pp, data))
else:
    print(b_testing(vocab1, vocab2, pp, data))
