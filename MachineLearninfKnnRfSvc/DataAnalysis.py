# Particular Data Analysis (with kNN) [1.2]
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score

#Params
from sklearn.svm import SVC

import warnings
warnings.simplefilter(action='ignore')
from MachineLearninfKnnRfSvc.ParameterKnnRfSvc import *

#Header in Outputfile
of=open(outputfilename,'a')
print('Particular Data Analysis (with kNN) [1.2]\n',file=of);
print(f"selected features: {featurecols}",file=of)
print(f"ignored lines: {linefilter}",file=of)
print(printseparator, file=of)


#Load Data
#Different Data, so we have to replace , with . and especially jump over the first line, because its strings
filedata=[str(line).replace(",", ".").split(inputseparator) for line in open(inputfilename).read().split("\n")[1:] if line != '']

#Filter Data
rawdata = [[filedata[j][i] for i in range(len(filedata[j])) if i in columnfilter or i==labelcolumn] for j in range(len(filedata)) if eval('j not in '+linefilter)]
print('count of data records: ',len(rawdata),'\n', file=of)

#Prepare Data
for l in range(len(rawdata)): 
   for i in range(columnflen): rawdata[l][i] = float(rawdata[l][i])

iris = pd.DataFrame.from_records(rawdata, columns=columnname)

#Function: distance of x and y
def distance(x,y):
   return pow(sum([abs(x[i]-y[i]) for i in range(len(x))]), 0.5)

dt={}  #Working Data; Select features
for i in range(len(rawdata)):
   dt[i] = {'features':[rawdata[i][k] for k in featurecols], 'label':rawdata[i][labelcolumn]}

#Calc Distance-Tables, sort them and do a first analysis on predictions
for i in range(len(dt)):
   dt[i]['dist'] = {j:distance(dt[i]['features'],dt[j]['features']) for j in range(len(dt)) if i!=j }
   dt[i]['sorted']= sorted([(e, dt[i]['label']==dt[e]['label']) for e in dt[i]['dist']], key=lambda sd: dt[i]['dist'][sd[0]], reverse=False)
   dt[i]['relpredict']=[(k, round([e[1] for e in dt[i]['sorted'][:k]].count(True) / float(k),rpdigits)) for k in range(1,len(dt[i]['sorted'])+1)]
   dt[i]['k_maxpred']=[e[1] for e in dt[i]['relpredict']].count(1.0)

#Show perdictions for nearest neighbours
for i in dt: print(f"{i:3} : {dt[i]['features']} - {dt[i]['label']} - KMP: {dt[i]['k_maxpred']} - {dt[i]['relpredict'][:firstrelpred]}", file=of)
print(printseparator, file=of)

#Show nodes with different nearest neighbours
print(f"Nodes with different first neighbours", file=of)
for d in dnnrange:
   print(f"KMP {d}: {[dt[i]['k_maxpred'] for i in range(len(dt))].count(d)} {[i for i in range(len(dt)) if dt[i]['k_maxpred']==d]}", file=of)


# columnname[['sepal_length', 'sepal_width']] = columnname[['sepal_length', 'sepal_width']].astype(float)

iris['fla'] = iris['sepal_length']*iris['sepal_width']

print(iris.head())

#create dataframes only species and without species
dataframe_features = iris.drop(columns = "species")

print(dataframe_features)

print(iris.info())

dataframe_species = iris.drop(columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "fla"])

#erstellen von Trainings- und Testdaten
print(dataframe_species)

X_train, X_test, y_train, y_test = train_test_split(dataframe_features, dataframe_species, test_size = 0.3)

print(X_train)

## Instantiate the model with 5 neighbors.
knn = KNeighborsClassifier(n_neighbors=5)

## Fit the model on the training data.
knn.fit(X_train, y_train)

## See how the model performs on the test data.
knn_score = knn.score(X_test, y_test)

svm = SVC(kernel='linear')
svm.fit(X_train, y_train)
Svm_score = svm.score(X_test, y_test)

# Instantiate model with decision trees
rf = RandomForestClassifier()
# Train the model on training data
rf.fit(X_train, y_train)
rf_score = rf.score(X_test, y_test)

knn_clf = KNeighborsClassifier()
rnd_clf = RandomForestClassifier()
svm_clf = SVC()
voting_clf = VotingClassifier(estimators=[('rf', rnd_clf), ('svc', svm_clf), ('knn', knn_clf)], voting='hard')
voting_clf.fit(X_train, y_train)
ensemble_score = voting_clf.score(X_test, y_test)

for clf in (knn_clf, rnd_clf, svm_clf):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(clf.__class__.__name__, accuracy_score(y_test, y_pred))

print("\n", file=of)
print("KNN                  :", knn_score, file=of)
print("SVM                  :", Svm_score, file=of)
print("Random Forest        :", rf_score, file=of)
print("Ensemble Learning    :", ensemble_score, file=of)
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", file=of)

# #bagging RandomForest
# bgrf = BaggingClassifier(RandomForestClassifier())
# bgrf.fit(X_train, y_train)
# print(bgrf.fit)
# print(bgrf.score(X_test, y_test))
#
# #bagging KNN
# bgknn = BaggingClassifier(KNeighborsClassifier())
# bgknn.fit(X_train, y_train)
# print(bgknn.fit)
# print(bgknn.score(X_test, y_test))
#
# #bagging SVM
# bgsvm = BaggingClassifier(SVC())
# bgsvm.fit(X_train, y_train)
# print(bgsvm.fit(X_train, y_train))
# print(bgsvm.score(X_test, y_test))
#Close up
of.close()