import os
from collections import Counter
import re
from collections import Counter
import numpy as np

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.metrics import confusion_matrix

#Funktionen definieren

def directoryliste(pfad, filter):
   pass

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


blacklist = ["spam123@hotmail.de"]
whitelist = ["ibimsderprof@hs-mannheim.de"]

def main():
    d = makeDict()
    features, labels = make_dataset(d)

    print (len(features), len(labels))

def makeDict():
    direc = "dir.nospam/"
    files = os.listdir(direc)

    emails = [direc + email for email in files]

    # print(files)


    words = []
    c = len(emails)
    for email in emails:
        f = open(email)
        blob = f.read()
        words += blob.split()
        print(c)
        c -= 1
        print(words)

    #delete all non alphabetic things
    for i in range(len(words)):
        if not words[i].isalpha():
            words[i] = ""
    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(20)

def make_dataset(dictionary):
    direc = "dir.nospam/"
    files = os.listdir(direc)

    emails = [direc + email for email in files]

    # print(files)
    feature_set = []
    labels = []
    c = len(emails)
    for email in emails:
        data = []
        f = open(email)
        words = f.read().split()
        for entry in dictionary:
            data.append(words.count(entry[0]))
        feature_set.append(data)
        if "ham" in email:
            labels.append(0)
        if "spam" in email:
            labels.append(1)
        print (c)
        c = c - 1
    return feature_set, labels


main()
#----------------------------------------------
#Vorbereitungen

#Parameter laden

#Blacklist laden

#Whitelist laden

#Spam-Mails laden und trainieren

#NoSpam-Mails laden und trainieren

#Bewertungstabellen mit Naive Bayes erstellen und in eigene Datei protokollieren

#----------------------------------------------
#MailInput laden, bewerten und nach MailOutput schreiben
#Bewertungsklassifikation: WhiteList, NoSpam, undetermined, Spam, BlackList

#Bewertungsübersicht fuer Mail-Eingang ausgeben



