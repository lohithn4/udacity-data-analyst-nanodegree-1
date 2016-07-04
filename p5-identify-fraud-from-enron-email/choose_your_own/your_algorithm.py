#!/usr/bin/python

import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture

features_train, labels_train, features_test, labels_test = makeTerrainData()


### the training data (features_train, labels_train) have both "fast" and "slow"
### points mixed together--separate them so we can give them different colors
### in the scatterplot and identify them visually
grade_fast = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==0]
bumpy_fast = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==0]
grade_slow = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==1]
bumpy_slow = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==1]


#### initial visualization
plt.xlim(0.0, 1.0)
plt.ylim(0.0, 1.0)
plt.scatter(bumpy_fast, grade_fast, color = "b", label="fast")
plt.scatter(grade_slow, bumpy_slow, color = "r", label="slow")
plt.legend()
plt.xlabel("bumpiness")
plt.ylabel("grade")
plt.show()
################################################################################


### your code here!  name your classifier object clf if you want the 
### visualization code (prettyPicture) to show you the decision boundary

from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

algs = ["Naive Bayes", "SVM", "Decision Tree", "AdaBoost", "Random Forest", "KNN"]

def classifier(alg_name):
    clf = None;    
    if(alg_name == "Naive Bayes"):
        clf = GaussianNB()
    elif(alg_name == "SVM"):
        clf = SVC(kernel="rbf", C=10000.)
    elif(alg_name == "Decision Tree"):
        clf = tree.DecisionTreeClassifier(min_samples_split = 40)
    elif(alg_name == "AdaBoost"):
        clf = AdaBoostClassifier(n_estimators=100)
    elif(alg_name == "Random Forest"):
        clf = RandomForestClassifier(n_estimators=10)
    else:
        clf = KNeighborsClassifier(n_neighbors=1)
    return clf
    
for alg_name in algs:
    clf = classifier(alg_name)
    clf.fit(features_train, labels_train) 
    pred = clf.predict(features_test)
    acc = accuracy_score(labels_test, pred)
    print alg_name, " accuracy: ", acc
    print
    '''    
    try:
        prettyPicture(clf, features_test, labels_test)
    except NameError:
        pass
    '''    
    print "==================="
    
