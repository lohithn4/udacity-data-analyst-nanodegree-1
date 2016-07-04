#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



### your code goes here 

from time import time
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size = 0.3, random_state = 42)

clf = tree.DecisionTreeClassifier()

t0 = time()
clf = clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"

t1 = time()
pred = clf.predict(features_test)
print "prediction time:", round(time()-t1, 3), "s"

acc = accuracy_score(labels_test, pred)

print acc

print len(pred)

zeroes = [0]*29
print accuracy_score(labels_test, zeroes)

true_positives = 0
false_positives = 0
false_negatives = 0

for pre, act in zip(pred, labels_test):
    pre = int(pre)
    act = int(act)
    if pre == 1 & act == 1:
        true_positives += 1
    elif pre == 1 & act == 0:
        false_positives += 1
    elif pre == 0 & act == 1:
        false_negatives += 1

print true_positives
print false_positives
print false_negatives

print precision_score(labels_test, pred)
print recall_score(labels_test, pred)


predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
true_labels2 = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]

print precision_score(true_labels2, predictions)
print recall_score(true_labels2, predictions)