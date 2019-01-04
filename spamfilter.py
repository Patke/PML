import os
import shutil

import pandas as pd

from nltk.classify import NaiveBayesClassifier
import random
import nltk
from collections import Counter

from pandas import DataFrame

from Parameter import *
import re
import operator

nltk.download('punkt')

path_current = os.path.dirname(os.path.abspath(__file__))
dir_noSpam = "C:\\Users\\Kevin\\PycharmProjects\\PML\\Spamfilter.Template\\dir.nospam"
dir_Spam = "C:\\Users\\Kevin\\PycharmProjects\\PML\\Spamfilter.Template\\dir.spam"
input_path = path_current + "/dir.mail.input/"

nsp_dict = []
spam_dict = []
nsp_list = []
spam_list = []

actualPath = os.path.dirname(os.path.abspath(__file__))
print(actualPath + dir_separator + dir_input)
rootdir = actualPath + dir_separator + "Spamfilter.Template"
print(list(char_replaces))

def create_word_features(words):
    my_dict = dict([(word, True) for word in words])
    return my_dict

# def read_input_emails():
#     inputPath = actualPath + dir_input
#     input_textlist = []
#     for directories, subdirs, files in os.walk(inputPath):
#             if (os.path.split(directories)[1] == 'dir.mail.input'):
#                 for filename in files:
#                     with open(os.path.join(directories, filename)) as f:
#                         print("test")
#                         input_text = f.read()
#                         input_textlist.append(input_text)
#     return input_textlist
#
# print(read_input_emails())



def create_lists_dicts():
    for directories, subdirs, files in os.walk(rootdir):
        if (os.path.split(directories)[1] == 'dir.nospam'):
            for filename in files:
                with open(os.path.join(directories, filename)) as f:
                        data = f.read()
                        matchNoSpamAll = []
                        matchNoSpam = re.findall(r'[\w\.-]+@[\w\.-]+', data)
                        matchNoSpamAll += matchNoSpam
                        # with open(filename_whitelist, "r") as my_file:
                        #     whitelist_text = my_file.read().replace('\n', "")
                        # if matchNoSpamAll[0] not in whitelist_text:
                        #     print("<" + matchNoSpamAll[0] + ">", file=open('whitelist', "a"))
                        for test in char_replaces.keys():
                            data = data.replace(test, ' ')

                        words = data.split()
                        nsp_dict.append((create_word_features(words), "dir.nospam"))
                        for i in words:
                            nsp_list.append(i)


        if (os.path.split(directories)[1] == 'dir.spam'):
            for filename in files:
                with open(os.path.join(directories, filename)) as f:
                        data = f.read()
                        matchSpamAll = []
                        matchSpam = re.findall(r'[\w\.-]+@[\w\.-]+', data)
                        matchSpamAll += matchSpam
                        # with open(filename_blacklist, "r") as my_file:
                        #     blacklist_text = my_file.read().replace('\n', "")
                        # if matchSpamAll[0] not in blacklist_text:
                        #     print("<" + matchSpamAll[0] + ">", file=open('blacklist', "a"))
                        for test in char_replaces.keys():
                            data = data.replace(test, ' ')

                        words = data.split()
                        spam_dict.append((create_word_features(words), "dir.spam"))
                        for i in words:
                            spam_list.append(i)

create_lists_dicts()
dict_countSpam = {}
dict_countNoSpam = {}
dict_countAll = {}
print("test")
print(dict_countSpam)
list_to = spam_list + nsp_list
# list_to = dict_countSpam.keys() + dict_countNoSpam.keys()


for word in list_to:
    dict_countAll[word] = dict_countAll.get(word, 0) + 1
for word in nsp_list:
    dict_countNoSpam[word] = dict_countNoSpam.get(word, 0) + 1
for word in spam_list:
    dict_countSpam[word] = dict_countSpam.get(word, 0) + 1
print(nsp_dict)
print(dict_countAll)
print(dict_countNoSpam)
print(dict_countNoSpam["Von"])
print(dict_countSpam)

list_allwords = list(dict_countSpam.keys()) + list(dict_countNoSpam.keys())
print(list_allwords)

# print("test2")

# sorted_countSpam = sorted(dict_countSpam.items(), key=operator.itemgetter(1))
# print(sorted_countSpam)
# print(Counter(list_to).most_common())
# print(nsp_dict[0])
# print(spam_dict[0])

# nsp = list(nsp_dict)
# print("test")
# print(nsp)
# d = {}
# for word in nsp:
#     d[word] = d.get(word, 0) + 1
# print("ich bin krass: " + d)
# # print(spam_list[0])


combined_list = nsp_dict + spam_dict
mail_list = []

def input_mail_list():
    for file in os.listdir(input_path):
        with open(input_path+file, 'r') as mail:
            mail_replaced = mail.read().replace("\n", "").replace("_", "").replace(".", "").replace("[", "").replace("]", "").replace(":", ""). replace(",", "").replace("/", "").replace("(", "").replace(")", "").replace(">", "").replace("<", "").replace(";", "").replace("\t", "")
            mail_list.append(mail_replaced)

input_mail_list()
print(mail_list)

def input_mail_einlesen():
    for directories, subdirs, files in os.walk(rootdir):
        if (os.path.split(directories)[1] == 'dir.mail.input'):
            for filename in files:
                with open(os.path.join(directories, filename)) as f:
                    input_text = f.read()
                return input_text


def trainieren():
    random.shuffle(combined_list)

    #Training Part ist 25, also 70% von 36
    training_part = int(len(combined_list) * .7)

    #Training Set wird dann 70% bekommen, also 25
    training_set = combined_list[:training_part]

    #Test Set bekommt 30%, also 11
    test_set = combined_list[training_part:]

    #Naive Bayes wird mit dem Training Set trainiert
    classifier = NaiveBayesClassifier.train(training_set)

    #Genauigkeit wid mit dem Test Set ausgerechnet
    accuracy = nltk.classify.util.accuracy(classifier, test_set)

    print("Accuracy is: ", accuracy)

    print(classifier.show_most_informative_features(100))

    return classifier

def get_email_adress():
    emailadress = re.findall(r'[\w\.-]+@[\w\.-]+', str(input_mail_einlesen()))
    return str(emailadress[0])


def mail_bewerten():
    if str(priorityorder[0]) is "whitelist":
        with open(filename_whitelist, "r") as file1:
            whitelist_text = file1.read().replace('\n', "")
        if (get_email_adress()) in whitelist_text:
            print("Address is in whiteList: NoSpam")
        with open(filename_blacklist, "r") as file2:
            blacklist_text = file2.read().replace('\n', "")
        if str(get_email_adress()) in blacklist_text:
            print("Address is in blacklist: Spam")
        else:
            words = nltk.word_tokenize(input_mail_einlesen())
            features = create_word_features(words)
            print("Message is:" + trainieren().classify(features), file=open(filename_results, "a"))


trainieren()



# Bewertungsklassifikation: WhiteList, NoSpam, undetermined, Spam, BlackList
# df = DataFrame()
dict_spamquotegesamt = {}
def create_ausgabe():
    df2 = DataFrame()
    # df_gesamtzahl = DataFrame()
    # df_zusammen = DataFrame()
    # df_spamquoteeinzeln = DataFrame()

    dict_gesamt = {}
    words = []
    for a in list_allwords:
        if a not in dict_countNoSpam:
            dict_countNoSpam[a] = 0
        if a not in dict_countSpam:
            dict_countSpam[a] = 0

        df = DataFrame({'Wort': [a], 'NoSpam': dict_countNoSpam[a], 'Spam': dict_countSpam[a]})
        df2 = df.append(df2, ignore_index=True)
        dict_gesamt[a] = (dict_countNoSpam[a] + dict_countSpam[a])
        # print(dict_countNoSpam[a])
        # print(dict_countSpam[a])
        # print(dict_gesamt[a])
        # df_gesamtzahl = df_zusammen.append(df_gesamtzahl, ignore_index=True)
        dict_spamquotegesamt[a] = (dict_countSpam[a])/(dict_gesamt[a])


    for email in mail_list:
        gesamt = 0
        counter = 0
        for word in email:
            if word in dict_spamquotegesamt:
                gesamt = gesamt + dict_spamquotegesamt[word]
                counter = counter +1

        rating = gesamt/counter
        print("Mail Rating:", gesamt/counter)


        if rating > 0.5:
            print("Spam")
        elif rating > 0.2 and rating < 0.5:
            print("undeterminded")
        else:
            print("NoSpam")

    print(dict_spamquotegesamt)
   # print(spam_email_bewertung)


    out = open(actualPath + dir_separator + "Spamfilter.Template" + dir_separator + dir_results + "spamfilterResults.txt", "w")
    out2 = open(actualPath + dir_separator + "Spamfilter.Template" + dir_separator + dir_results + "spamfilterResults.txt", "w")
    print(df2.sort_values(by=['NoSpam']), file=out)
    print(dict_spamquotegesamt, file=out)
    print(words)
    print(dict_spamquotegesamt)
    print(len(dict_spamquotegesamt))
    # print(spamquote)
    print(actualPath + dir_separator + "Spamfilter.Template" + dir_separator + dir_results + "\\spamfilterResults.txt")

    out.close()

print("Hallo", spam_list)
            # df_spamquoteeinzeln = DataFrame({'Wort': [a], 'Spamquote': (dict_countSpam[a])/(df_Gesamtzahl[a])})
            # df_spamquotegesamt = df_spamquoteeinzeln.append(df_spamquotegesamt, ignore_index=True)

    # print(df_gesamtzahl['listinfo'])
    # print(df_spamquotegesamt)

create_ausgabe()

# get_email_adress()

mail_bewerten()

# shutil.copy(actualPath + dir_separator + "Parameter.py", actualPath + dir_separator + "Spamfilter.Template" + dir_separator + dir_results)

print(dict_spamquotegesamt)