import os
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

# Funktionen definieren
rootdir = "C:\\Users\\Kevin\\PycharmProjects\\PML\\Spamfilter.Template"
dir_noSpam = "C:\\Users\\Kevin\\PycharmProjects\\PML\\Spamfilter.Template\\dir.nospam"
dir_Spam = "C:\\Users\\Kevin\\PycharmProjects\\PML\\Spamfilter.Template\\dir.spam"


def directoryliste(pfad, filter):
    for directories, subdirs, files in os.walk(rootdir):
        if (os.path.split(directories)[1] == "dir.nospam"):
            print(directories, subdirs, len(files))
        if (os.path.split(directories)[1] == "dir.spam"):
            print(directories, subdirs, len(files))

print(directoryliste(rootdir, filter))

nsp_dict = []
spam_dict = []
nsp_list = []
spam_list = []


def create_word_features(words):
    my_dict = dict([(word, True) for word in words])
    return my_dict


char_replaceList = list(char_replaces.keys())
# print(char_replaceList)
# print(char_replaceList[1])
# for a in char_replaceList:
#     print(repr(a))

for directories, subdirs, files in os.walk(rootdir):
    if (os.path.split(directories)[1] == 'dir.nospam'):
        for filename in files:
            with open(os.path.join(directories, filename)) as f:
                    data = f.read()
                    matchNoSpamAll = []
                    matchNoSpam = re.findall(r'[\w\.-]+@[\w\.-]+', data)
                    matchNoSpamAll += matchNoSpam
                    with open(filename_whitelist, "r") as my_file:
                        whitelist_text = my_file.read().replace('\n', "")
                    if matchNoSpamAll[0] not in whitelist_text:
                        print("<" + matchNoSpamAll[0] + ">", file=open('whitelist', "a"))
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
                    matchSpam = re.findall(r'[\w\.-]+@[\w\.-]+', data)
                    matchSpamAll = []
                    matchSpam = re.findall(r'[\w\.-]+@[\w\.-]+', data)
                    matchSpamAll += matchSpam
                    with open(filename_blacklist, "r") as my_file:
                        blacklist_text = my_file.read().replace('\n', "")
                    if matchSpamAll[0] not in blacklist_text:
                        print("<" + matchSpamAll[0] + ">", file=open('blacklist', "a"))
                    for test in char_replaces.keys():
                        data = data.replace(test, ' ')

                    words = data.split()
                    spam_dict.append((create_word_features(words), "dir.spam"))
                    for i in words:
                        spam_list.append(i)

# print("test")
# print(nsp_list)
# print(spam_list)
print(nsp_dict)
list_to = nsp_list + spam_list

dict_countSpam = {}
dict_countNoSpam = {}
dict_countAll = {}
for word in list_to:
    dict_countAll[word] = dict_countAll.get(word, 0) + 1
for word in nsp_list:
    dict_countNoSpam[word] = dict_countNoSpam.get(word, 0) + 1
for word in spam_list:
    dict_countSpam[word] = dict_countSpam.get(word, 0) + 1

# print("test2")
print(dict_countAll)
print(dict_countNoSpam)
print(dict_countNoSpam["Von"])
sorted_countSpam = sorted(dict_countSpam.items(), key=operator.itemgetter(1))
print(sorted_countSpam)
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


inputPath = "C:\\Users\\Kevin\\PycharmProjects\\PML\\Spamfilter.Template\\dir.mail.input"
for directories, subdirs, files in os.walk(inputPath):
    if (os.path.split(directories)[1] == 'dir.mail.input'):
        for filename in files:
            with open(os.path.join(directories, filename)) as f:
                input_text = f.read()


words = nltk.word_tokenize(input_text)
features = create_word_features(words)
print("Message 1 is :" + classifier.classify(features))

# Bewertungsklassifikation: WhiteList, NoSpam, undetermined, Spam, BlackList
# df = DataFrame()
df2 = DataFrame()
x = 0
for a in list_to:
    if a not in dict_countNoSpam:
        dict_countNoSpam[a] = 0
    if a not in dict_countSpam:
        dict_countSpam[a] = 0

        df = DataFrame({'Wort': [a], 'NoSpam': dict_countNoSpam[a], 'Spam': dict_countSpam[a]})
        df2 = df.append(df2, ignore_index=True)
print(df2.sort_values(by=['NoSpam']))




def maildatei_laden(dateiname):
    pass


def maildatei_schreiben(dateiname, email):
    pass


def mail_header(mail):
    pass


def mail_body(mail):
    pass


def mail_bewerten(mail):
    pass

# blacklist = ["spam123@hotmail.de"]
# whitelist = ["ibimsderprof@hs-mannheim.de"]
#
# def main():
#     d = makeDict()
#     features, labels = make_dataset(d)
#
#     print (len(features), len(labels))
#
# def makeDict():
#     direc = "dir.nospam/"
#     files = os.listdir(direc)
#
#     emails = [direc + email for email in files]
#
#     # print(files)
#
#
#     words = []
#     c = len(emails)
#     for email in emails:
#         f = open(email)
#         blob = f.read()
#         words += blob.split()
#         print(c)
#         c -= 1
#         print(words)
#
#     #delete all non alphabetic things
#     for i in range(len(words)):
#         if not words[i].isalpha():
#             words[i] = ""
#     dictionary = Counter(words)
#     del dictionary[""]
#     return dictionary.most_common(20)
#
# def make_dataset(dictionary):
#     direc = "dir.nospam/"
#     files = os.listdir(direc)
#
#     emails = [direc + email for email in files]
#
#     # print(files)
#     feature_set = []
#     labels = []
#     c = len(emails)
#     for email in emails:
#         data = []
#         f = open(email)
#         words = f.read().split()
#         for entry in dictionary:
#             data.append(words.count(entry[0]))
#         feature_set.append(data)
#         if "ham" in email:
#             labels.append(0)
#         if "spam" in email:
#             labels.append(1)
#         print (c)
#         c = c - 1
#     return feature_set, labels
#
#
# main()
# ----------------------------------------------
# Vorbereitungen

# Parameter laden

# Blacklist laden

# Whitelist laden

# Spam-Mails laden und trainieren

# NoSpam-Mails laden und trainieren

# Bewertungstabellen mit Naive Bayes erstellen und in eigene Datei protokollieren

# ----------------------------------------------
# MailInput laden, bewerten und nach MailOutput schreiben
# Bewertungsklassifikation: WhiteList, NoSpam, undetermined, Spam, BlackList

# Bewertungsübersicht fuer Mail-Eingang ausgeben
