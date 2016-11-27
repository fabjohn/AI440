import math
import sys
def open_training_set():
    with open("fisher_train_40topic.txt")as f:
        train = f.read().splitlines()
    return train

def multi_nb_training(train):
    dict_list = [0]*40
    count_list = [0]*40
    wordsum_list = [0]*40
    class_p = [0]*40
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
                wordsum_list[topic] += int(temp[1])
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
                wordsum_list[topic] += int(temp[1])
            dict_list[topic] = cur_dict
    # only create a dict to add zero to complete other topic's dict
    complete_dict = {}
    for n in range(40):
        topic = dict_list[n]
        for word in topic:
            if word not in complete_dict:
                complete_dict[word] = 0
    # print(complete_dict)
    # print(len(complete_dict))
    # expand the incomplete topic
    for n in range(40):
        topic = dict_list[n]
        for word in complete_dict:
            if word not in topic:
                topic[word] = 0

    for n in range(40):
        class_p[n] = count_list[n]/10244        #total of 10244 documents.
        topic = dict_list[n]
        for word in topic:
            topic[word] = math.log((topic[word]+1)/(wordsum_list[n]+len(topic)))
    return dict_list, class_p

def bernoulli_nb(train):
    topic_dict = {}
    for n in range(40):
        topic_dict[n] = 0

    count_list = [0]*40
    class_p = [0]*40
    for row in train:
        currow = row.split(' ')
        topic = int(currow[0])
        if topic_dict[topic] == 0:
            cur_dict = {}
            count_list[topic] += 1
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in cur_dict:
                    cur_dict[temp[0]] = 0
                cur_dict[temp[0]] += 1
            topic_dict[topic] = cur_dict
        else:
            count_list[topic] += 1
            cur_dict = topic_dict[topic]
            del currow[0]
            for word in currow:
                temp = word.split(':')
                if temp[0] not in cur_dict:
                    cur_dict[temp[0]] = 0
                cur_dict[temp[0]] += 1
            topic_dict[topic] = cur_dict
    # only create a dict to add zero to complete other topic's dict
    complete_dict = {}
    for n in range(40):
        topic = topic_dict[n]
        for word in topic:
            if word not in complete_dict:
                complete_dict[word] = 0
    # print(complete_dict)
    # print(len(complete_dict))
    # expand the incomplete topic
    for n in range(40):
        topic = topic_dict[n]
        for word in complete_dict:
            if word not in topic:
                topic[word] = 0
    for n in range(40):
        class_p[n] = count_list[n]/10244        #total of 10244 documents.
        topic = topic_dict[n]
        for word in topic:
            topic[word] = [math.log((topic[word]+1)/(count_list[n]+2)),math.log((count_list[n]-topic[word]+1)/(count_list[n]+2))]
    return topic_dict, class_p

#
# def bernoulli_nb(train):
#     d1v = {}        #positive dict
#     d2v = {}        #negative dict
#     sum1 = 0        #total positive reviews
#     sum2 = 0        #total negative reviews
#     pcount = 0
#     ncount =0
#     for row in train:
#         currow = row.split(' ')
#         if currow[0] == '1': #positve review
#             pcount += 1
#             del currow[0]
#             for word in currow:
#                 temp = word.split(':')
#                 if temp[0] not in d1v:
#                     d1v[temp[0]] = 0
#                 d1v[temp[0]] += 1       #wordcount doesn't matter
#             #sum1 += 1       #count one positve review
#         else:               #negative review
#             ncount +=1
#             del currow[0]
#             for word in currow:
#                 temp = word.split(':')
#                 if temp[0] not in d2v:
#                     d2v[temp[0]] = 0
#                 d2v[temp[0]] += 1
#             #sum2 += 1
#     for key in d1v:
#         if key not in d2v:
#             d2v[key] = 0
#     for key in d2v:
#         if key not in d1v:
#             d1v[key] = 0
#     # v = len(d1v)
#     # for key, value in d1v.items():
#     #     d1v[key] = math.log((d1v[key]+1)/(pcount+v))
#     # for key, value in d2v.items():
#     #     d2v[key] = math.log((d2v[key]+1)/(ncount+v))
#     v = len(d1v)
#     for key in d1v:
#         d1v[key] = [math.log((d1v[key]+1)/(pcount+v)),math.log((pcount-d1v[key]+1)/(pcount+v))]
#     for key in d2v:
#         d2v[key] = [math.log((d2v[key]+1)/(ncount+v)),math.log((ncount-d2v[key]+1)/(ncount+v))]
#     pp = (pcount)/(pcount+ncount)
#     return d1v, d2v, pp


def m_testing(topic_list, class_p):
    with open("fisher_test_40topic.txt")as f:
            test = f.read().splitlines()
    correct = 0
    wrong = 0
    mtx = [0]*40        ##topic
    for n in range(40):
        col = [0]*40
        mtx[n]= col
    for row in test:
        currow = row.split(' ')
        topic = int(currow[0])
        del currow[0]
        sum = [0]*40
        laplace = [0]*40
        max = -sys.maxsize-1
        max_t = 0
        for word in currow:
            temp = word.split(':')
            if temp[0] in topic_list[0]:
                for n in range(40):
                    cur_topic = topic_list[n]
                    sum[n] += cur_topic[temp[0]]*int(temp[1])
        for n in range(40):
            laplace[n] = math.log(class_p[n])+sum[n]
            if laplace[n] > max:
                max = laplace[n]
                max_t = n
        temp = mtx[topic]
        temp[max_t] += 1
        if max_t != topic:
            wrong +=1
        else:
            correct += 1
    for row in mtx:
        counter = -sys.maxsize-1
        nsum = 0
        for n in range(40):
            nsum += row[n]
        for n in range(40):
            row[n] = row[n]/nsum
        for n in range(40):
            if row[n]>counter:
                counter = row[n]
                key_v = n
        del row[key_v]
        counter= -sys.maxsize-1
        for n in range(39):
            if row[n] > counter:
                counter = row[n]
                sec_high = n
        print(sec_high)
    for row in mtx:
        print(row)
    accuracy = correct/(correct+wrong)
    return accuracy


def b_testing(topic_dict, class_p):
    with open("fisher_test_40topic.txt")as f:
            test = f.read().splitlines()
    correct = 0
    wrong = 0
    mtx = [0]*40        ##topic
    for n in range(40):
        col = [0]*40
        mtx[n]= col
    for row in test:
        currow = row.split(' ')
        topic = int(currow[0])
        del currow[0]
        sum = [0]*40
        laplace = [0]*40
        max = -sys.maxsize -1
        max_t = 0
        doc_word = {}
        for word in currow:
            temp = word.split(':')
            word = temp[0]
            if word in topic_dict[0]:       #random dict since they have same keys.
                doc_word[word] = 0       #only append when word in the dictionary
        print(doc_word)
        for vocab in topic_dict[0]:
            for n in topic_dict:
                cur_dict = topic_dict[n]
                cur_word = cur_dict[vocab]
                if vocab in doc_word:           #if the dictionary word occurs at current document
                    sum[n] += cur_word[0]
                else:
                    sum[n] += cur_word[1]
        for n in range(40):
            laplace[n] = math.log(class_p[n])+sum[n]
            if laplace[n] > max:
                max = laplace[n]
                max_t = n
        count = mtx[topic]
        count[max_t] += 1
        if max_t != topic:
            wrong +=1
        else:
            correct += 1
    for row in mtx:
        nsum = 0
        for n in range(40):
            nsum += row[n]
        for n in range(40):
            row[n] = row[n]/nsum

    for row in mtx:
        print(row)

    accuracy = correct/(correct+wrong)
    return accuracy


# #
type = input('enter the model you want to use:(1 is Multinomial, 2 is Bernoulli)')
##data = input('enter the corpora you wnat to review:(1 is Movie, 2 is Convo topic)')

train = open_training_set()
if type == '1':
    topic_list, p_class = multi_nb_training(train)
    print(m_testing(topic_list, p_class))
else:
    topic_list, p_class = bernoulli_nb(train)
    print(b_testing(topic_list, p_class))


