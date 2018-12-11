# Particular Data Analysis (with kNN) [1.2]

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
## Import the Classifier.
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn import svm
import numpy as np


#Params
from sklearn.svm import SVC

inputfilename  = 'iris.data'                  #filename input data
outputfilename = inputfilename + '.erg'       #filename output data
inputseparator = ','                          #separator for csv columns
labelcolumn    = 4                            #column of label
columnfilter   = [0,1,2,3]                    #columns with features
columnflen     = len(columnfilter)            #count of features in data
featurecols    = [0,1,2,3]                    #selected Features
linefilter     = '[]'                         #linefilter: lines to ignore
firstrelpred   = 10                           #count of first neighbours in outputlist
rpdigits       = 4                            #relative prediction: number of digits after decimal point
dnnrange       = [0,1,2,3,4]                  #show different nearest neighbour range 
printseparator = '*'*80+'\n'
columnname = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]

#Header in Outputfile
of=open(outputfilename,'w')
print('Particular Data Analysis (with kNN) [1.2]\n',file=of);
print(f"selected features: {featurecols}",file=of)
print(f"ignored lines: {linefilter}",file=of)
print(printseparator, file=of)

#Load Data
filedata=[line.split(inputseparator) for line in open(inputfilename).read().split("\n") if line != '']

#Filter Data
rawdata = [[filedata[j][i] for i in range(len(filedata[j])) if i in columnfilter or i==labelcolumn] for j in range(len(filedata)) if eval('j not in '+linefilter)]
print('count of data records: ',len(rawdata),'\n', file=of)

#Prepare Data
for l in range(len(rawdata)): 
   for i in range(columnflen): rawdata[l][i] = float(rawdata[l][i])

iris = pd.DataFrame.from_records(rawdata, columns=columnname)


# columnname[['sepal_length', 'sepal_width']] = columnname[['sepal_length', 'sepal_width']].astype(float)
iris['fla'] = iris['sepal_length']*iris['sepal_width']

print(iris.head())

dataframe_features = iris.drop(columns = "species")

print(dataframe_features)

print(iris.info())

dataframe_species = iris.drop(columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", "fla"])

print(dataframe_species)

X_train, X_test, y_train, y_test = train_test_split(dataframe_features, dataframe_species, test_size = 0.3)

print(X_train)

## Instantiate the model with 5 neighbors.
knn = KNeighborsClassifier(n_neighbors=5)

## Fit the model on the training data.
knn.fit(X_train, y_train)

## See how the model performs on the test data.
knn.score(X_test, y_test)

print(knn.score(X_test, y_test))

clf = SVC(kernel='linear')
clf.fit(X_train, y_train)
Svm_score = clf.score(X_train, y_train)
print(Svm_score)

# Instantiate model with 1000 decision trees
rf = RandomForestClassifier()
# Train the model on training data
rf.fit(X_train, y_train)
rf_score = rf.score(X_test, y_test)
print(rf_score)

#create a dictionary of all values we want to test for n_estimators
params_rf = {"n_estimators": [50, 100, 200]}
#use gridsearch to test all values for n_estimators
rf_gs = GridSearchCV(rf, params_rf, cv=5)
#fit model to training data
rf_gs.fit(X_train, y_train)

#save best model
rf_best = rf_gs.best_estimator_
#check best n_estimators value
print(rf_gs.best_params_)

#create a dictionary of all values we want to test for n_neighbors
params_knn = {"n_neighbors": np.arange(1, 25)}
#use gridsearch to test all values for n_neighbors
knn_gs = GridSearchCV(knn, params_knn, cv=5)
#fit model to training data
knn_gs.fit(X_train, y_train)
#create a dictionary of our models

#save best model
knn_best = knn_gs.best_estimator_
#check best n_neigbors value
print(knn_gs.best_params_)

estimators=[("knn", knn_best), ("rf", rf_best)]
print(estimators)

#create our voting classifier, inputting our models
ensemble = VotingClassifier(estimators, voting="hard")

#fit model to training data
ensemble.fit(X_train, y_train)
#test our model on the test data
ensemble_wert = ensemble.score(X_test, y_test)

print("test")
print(ensemble_wert)

# #Function: distance of x and y
# def distance(x,y):
#    return pow(sum([abs(x[i]-y[i]) for i in range(len(x))]), 0.5)
#
# dt={}  #Working Data; Select features
# for i in range(len(rawdata)):
#    dt[i] = {'features':[rawdata[i][k] for k in featurecols], 'label':rawdata[i][labelcolumn]}
#
# #Calc Distance-Tables, sort them and do a first analysis on predictions
# for i in range(len(dt)):
#    dt[i]['dist'] = {j:distance(dt[i]['features'],dt[j]['features']) for j in range(len(dt)) if i!=j }
#    dt[i]['sorted']= sorted([(e, dt[i]['label']==dt[e]['label']) for e in dt[i]['dist']], key=lambda sd: dt[i]['dist'][sd[0]], reverse=False)
#    dt[i]['relpredict']=[(k, round([e[1] for e in dt[i]['sorted'][:k]].count(True) / float(k),rpdigits)) for k in range(1,len(dt[i]['sorted'])+1)]
#    dt[i]['k_maxpred']=[e[1] for e in dt[i]['relpredict']].count(1.0)
#
# #Show perdictions for nearest neighbours
# for i in dt: print(f"{i:3} : {dt[i]['features']} - {dt[i]['label']} - KMP: {dt[i]['k_maxpred']} - {dt[i]['relpredict'][:firstrelpred]}", file=of)
# print(printseparator, file=of)
#
# #Show nodes with different nearest neighbours
# print(f"Nodes with different first neighbours", file=of)
# for d in dnnrange:
#    print(f"KMP {d}: {[dt[i]['k_maxpred'] for i in range(len(dt))].count(d)} {[i for i in range(len(dt)) if dt[i]['k_maxpred']==d]}", file=of)
#
# #Close up
# of.close()

