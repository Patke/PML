import os
from pandas import DataFrame
from Parameter import *
import re



path_current = os.path.dirname(os.path.abspath(__file__))
dir_noSpam = path_current + dir_separator + "dir.nospam"
dir_Spam = path_current + dir_separator + "dir.spam"
input_path = path_current + dir_separator + "Spamfilter" + "/dir.mail.input/"

nsp_dict = []
spam_dict = []
nsp_list = []
spam_list = []

actualPath = os.path.dirname(os.path.abspath(__file__))
rootdir = actualPath + dir_separator + "Spamfilter"
log_output = open(actualPath + dir_separator + "Spamfilter" + dir_separator + "dir.filter.results" + dir_separator + "spamfilter.log.txt", "w")

def create_word_features(words):
    my_dict = dict([(word, True) for word in words])
    return my_dict


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
list_to = spam_list + nsp_list



for word in list_to:
    dict_countAll[word] = dict_countAll.get(word, 0) + 1
for word in nsp_list:
    dict_countNoSpam[word] = dict_countNoSpam.get(word, 0) + 1
for word in spam_list:
    dict_countSpam[word] = dict_countSpam.get(word, 0) + 1

list_allwords = list(dict_countSpam.keys()) + list(dict_countNoSpam.keys())

mail_list = []

def input_mail_list():
    for file in os.listdir(input_path):
        with open(input_path+file, 'r') as mail:
            mail_replaced = mail.read().replace("\n", "").replace("_", "").replace(".", "").replace("[", "").replace("]", "").replace(":", ""). replace(",", "").replace("/", "").replace("(", "").replace(")", "").replace(">", "").replace("<", "").replace(";", "").replace("\t", "")
            mail_list.append(mail_replaced)

input_mail_list()

def input_mail_einlesen():
    for directories, subdirs, files in os.walk(rootdir):
        if (os.path.split(directories)[1] == 'dir.mail.input'):
            for filename in files:
                with open(os.path.join(directories, filename)) as f:
                    input_text = f.read()
                return input_text


def get_email_adress():
    emailadress = re.findall(r'[\w\.-]+@[\w\.-]+', str(input_mail_einlesen()))
    return str(emailadress[0])


dict_spamquotegesamt = {}

def create_ausgabe():
    df2 = DataFrame()
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
        dict_spamquotegesamt[a] = (dict_countSpam[a])/(dict_gesamt[a])

    rating_list = []

    for email in mail_list:
        gesamt = 0
        counter = 0
        for word in email.split():
            if word in dict_spamquotegesamt:
                gesamt = gesamt + dict_spamquotegesamt[word]
                counter = counter + 1

        rating = gesamt/counter


        if rating > 0.5:
            rating_list.append((rating, "Spam"))
        elif rating > 0.2 and rating < 0.5:
            rating_list.append((rating, "undetermined"))
        else:
            rating_list.append((rating, "NoSpam"))

    for email in mail_list:
        with open(filename_blacklist, "r") as my_file:
                blacklist_text = my_file.read().replace('\n', "").split()
                for line in blacklist_text:
                    if line in email:
                            print(line + ": " +"Mail in Blacklist", file=log_output)
                            break
        with open(filename_whitelist, "r") as my_file:
                whitelist_text = my_file.read().replace('\n', "").split()
                for line in whitelist_text:
                    if line in email:
                            print("Mail in Whitelist")
                            break

    out = open(actualPath + dir_separator + "Spamfilter" + dir_separator + "dir.filter.results" + dir_separator + "nb.wordtable.txt","w")
    print(df2.sort_values(by=['NoSpam']), file=out)
    out.close()

    return rating_list


rating_list = create_ausgabe()


for idx, mail in enumerate(mail_list):
    output = open(actualPath + dir_separator + "Spamfilter" + dir_separator + "dir.mail.output" + dir_separator + mail[3:20]+".txt", "w")
    print("XSpamProbability:   " + str(rating_list[idx][0]) + "             " +"XSpam:   " + rating_list[idx][1], file= output)

    with open(filename_blacklist, "r") as my_file:
            blacklist_text = my_file.read().replace('\n', "").split()
            for line in blacklist_text:
                if line in mail:
                        print("XSpam: Blacklist ", file=output)
                        break
    with open(filename_whitelist, "r") as my_file:
            whitelist_text = my_file.read().replace('\n', "").split()
            for line in whitelist_text:
                if line in mail:
                        print("Mail in Whitelist")
                        print("XSpam: Whitelist ", file=output)
                        break


    print(mail, file=output)

output_bewertung = open(actualPath + dir_separator + "Spamfilter" + dir_separator + "dir.filter.results" + dir_separator + "spamfilter.results.txt", "w")

print("Auswertepriorität: blacklist, whitelist, naive_bayes" + "    " + "Klassifizierungsgrenzen: spam (1.0 bis 0.5), undetermined (0,5 bis 0,2) und nospam [0,2 bis 0.0]", file=output_bewertung)
print("*******************************************************************************************************************************************************************", file= output_bewertung)
print("*******************************************************************************************************************************************************************", file= log_output)
for idx, mail in enumerate(mail_list):
    print(mail[3:20] + "    " + "XSpamProbability:  " + str(rating_list[idx][0]) + "  " + "XSpam:   " + rating_list[idx][1], file=output_bewertung)
    print(mail[3:20] + "    " + "XSpamProbability:  " + str(rating_list[idx][0]) + "  " + "XSpam:   " + rating_list[idx][1], file=log_output)


