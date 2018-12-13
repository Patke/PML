import os
from nltk.classify import NaiveBayesClassifier
import random
import nltk
from collections import Counter
from Parameter import *

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
print(char_replaceList)
print(char_replaceList[1])
for directories, subdirs, files in os.walk(rootdir):
    if (os.path.split(directories)[1] == 'dir.nospam'):
        for filename in files:
            with open(os.path.join(directories, filename)) as f:
                    data = f.read()
                # The data we read is one big string. We need to break it into words.
                    words = data.split()
                    nsp_dict.append((create_word_features(words), "dir.nospam"))
            for i in words:
                nsp_list.append(i)
                # for i in words:
                #     if "@" in i:
                #         print("Thats the right row: " + i)

    if (os.path.split(directories)[1] == 'dir.spam'):
        for filename in files:
            with open(os.path.join(directories, filename)) as f:
                    data = f.read()
                    words = data.split()
                    spam_dict.append((create_word_features(words), "dir.spam"))
            for i in words:
                spam_list.append(i)

print("test")
print(nsp_list)
print(spam_list)

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

print("test2")
print(dict_countAll)
print(dict_countNoSpam)
print(dict_countSpam)
print(Counter(list_to).most_common())
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
print(len(combined_list))
random.shuffle(combined_list)

training_part = int(len(combined_list) * .7)
print(len(combined_list))
training_set = combined_list[:training_part]
test_set = combined_list[training_part:]

print(len(training_set))
print(len(test_set))

classifier = NaiveBayesClassifier.train(combined_list)

accuracy = nltk.classify.util.accuracy(classifier, test_set)

print("Accuracy is: ", accuracy)

print(classifier.show_most_informative_features(100))


# inputPath = "C:\\Users\\Kevin\\PycharmProjects\\PML\\Spamfilter.Template\\dir.mail.input"
# for directories, subdirs, files in os.walk(inputPath):
#     if (os.path.split(directories)[1] == 'dir.mail.input'):
#         for filename in files:
#             with open(os.path.join(directories, filename)) as f:
#                 input_text = f.read()
#
# print("That's the inputtext: " + input_text)
#
# words = nltk.word_tokenize(input_text)
# features = create_word_features(words)
# print("Message 1 is :" + classifier.classify(features))


# print(training_set)
# print(spam_list)


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
