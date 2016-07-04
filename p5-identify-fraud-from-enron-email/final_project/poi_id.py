#!/usr/bin/python

import sys
import pickle

from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import SGDClassifier

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


############################################################################
### Task 1: Select what features you'll use.                             ###
### features_list is a list of strings, each of which is a feature name. ###
### The first feature must be "poi".                                     ###
############################################################################

financial_features = ['salary', 
                      'deferral_payments', 
                      'total_payments', 
                      'loan_advances', 
                      'bonus', 
                      'restricted_stock_deferred', 
                      'deferred_income', 
                      'total_stock_value', 
                      'expenses', 
                      'exercised_stock_options', 
                      'other', 
                      'long_term_incentive', 
                      'restricted_stock', 
                      'director_fees']

email_features     = ['to_messages', 
                      #'email_address', 
                      'from_poi_to_this_person', 
                      'from_messages', 
                      'from_this_person_to_poi', 
                      'shared_receipt_with_poi'] 

# I'll start with ALL features and then select only the best ones
features_list = ['poi'] + financial_features + email_features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

###############################
### Task 2: Remove outliers ###
###############################

outliers = ["TOTAL", 
            "THE TRAVEL AGENCY IN THE PARK"]
for o in outliers:
    data_dict.pop(o,0)
    
#####################################
### Task 3: Create new feature(s) ###
#####################################

# Two new features:
# 1) ratio_to_poi   = from_this_person_to_poi / to_messages
# 2) ratio_from_poi = from_poi_to_this_person / from_messages

my_new_features = ["ratio_to_poi", 
                   "ratio_from_poi"]

#features_list += my_new_features

for item in data_dict:
    person = data_dict[item]
    
    # New feature 1: ratio_to_poi
    #---------------------------
    if person["from_this_person_to_poi"] == 'NaN' or person["to_messages"] == 'NaN':
        person["ratio_to_poi"] = 'NaN'
    else:
        person["ratio_to_poi"] = float(person["from_this_person_to_poi"]) / float(person["to_messages"])
    
    # New feature 2: ratio_from_poi
    #------------------------------
    if person["from_poi_to_this_person"] == 'NaN' or person["from_messages"] == 'NaN':
        person["ratio_from_poi"] = 'NaN'
    else:
        person["ratio_from_poi"] = float(person["from_poi_to_this_person"]) / float(person["from_messages"])

##############################################       
### Select best features using SelectKBest ###
##############################################

# Add engineered features to the feature list
features_list = features_list + ['ratio_to_poi', 'ratio_from_poi']

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

k = 15
kbest = SelectKBest(k=k)
kbest.fit(features, labels)

scores = kbest.scores_
unsorted = zip(features_list[1:], scores)
k_best_features = list(reversed(sorted(unsorted, key=lambda x: x[1])))

# New list of the best features
best_features_list = ["poi"] + dict(k_best_features[:k]).keys()

# Update feature list to have the best k features (including engineered ones)
features_list = best_features_list

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list)
labels, features = targetFeatureSplit(data)

###########################################
### Scaling features using MinMaxScaler ###
###########################################

scaler = MinMaxScaler()
features = scaler.fit_transform(features)

########################################################################
### Task 4: Try a varity of classifiers                              ###
### Please name your classifier clf for easy export below.           ###
### Note that if you want to do PCA or other multi-stage operations, ###
### you'll need to use Pipelines. For more info:                     ### 
### http://scikit-learn.org/stable/modules/pipeline.html             ###
########################################################################
        
# Returns a classifier and params based on the algorithm name
def get_classifier_and_params(alg_name):

    clf = None
    params = {}    
    
    if(alg_name == "SVM"):
        params = {'kernel':('linear', 'rbf'), 'C':[1., 10., 100., 10000.]}
        clf = SVC()    
    elif(alg_name == "Decision Tree"):
        params = {"min_samples_split":[2, 5, 10, 20, 40], "criterion": ('gini', 'entropy')}
        clf = tree.DecisionTreeClassifier()    
    elif(alg_name == "AdaBoost"):
        params = {"n_estimators":[20, 25, 30, 40, 50, 200], 'algorithm': ('SAMME', 'SAMME.R')}
        clf = AdaBoostClassifier()    
    elif(alg_name == "Random Forest"):
        params = {"n_estimators":[2, 3, 5, 10], "criterion": ('gini', 'entropy')}
        clf = RandomForestClassifier()    
    elif(alg_name == "KNN"):
        params = {"n_neighbors":[1, 2, 5], "p":[2,3]}
        clf = KNeighborsClassifier()    
    elif(alg_name == 'KMeans'):
        params = {"n_clusters":[2], "n_init":[10,20,40]}
        clf = KMeans()
    elif(alg_name == 'SGD'):
        params = {"loss": ['log']}
        clf = SGDClassifier()
        
    return clf, params
    
#############################################################################################################
### Task 5: Tune your classifier to achieve better than .3 precision and recall                           ###
### using our testing script. Check the tester.py script in the final project                             ###
### folder for details on the evaluation method, especially the test_classifier                           ###
### function. Because of the small size of the dataset, the script uses                                   ###
### stratified shuffle split cross validation. For more info:                                             ###
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html ###
#############################################################################################################

# List of algorithms to be tested
algs = [
        "SVM", 
        "Decision Tree", 
        "AdaBoost", 
        "Random Forest", 
        "KNN",
        #"KMeans",
        "SGD"
        ]

    
# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42, stratify=labels)

# Go through all algorithms, tune and evaluate
for alg_name in algs:

    pre_clf, params = get_classifier_and_params(alg_name)
    
    # Tune classifier paramters with GridSearchCV
    clf = GridSearchCV(pre_clf, params, scoring='recall')
    clf = clf.fit(features_train, labels_train)
    best_p = clf.best_params_    
    clf = clf.best_estimator_

    pred = clf.predict(features_test)

    f1 = f1_score(labels_test, pred)
    recall = recall_score(labels_test, pred)
    precision = precision_score(labels_test, pred)
    accuracy = accuracy_score(labels_test, pred)
    
    print "==============="
    print "Algorithm: ", alg_name
    print "Params: ", best_p
    print "accuracy: ", accuracy
    print "f1: ", f1
    print "recall: ", recall
    print "precision: ", precision
   
###############################################################     
### Best classifier:                                        ###
### Set manually after testing                              ###
###############################################################

clf = AdaBoostClassifier(n_estimators = 200, algorithm = 'SAMME.R')

###################################################################################
### Task 6: Dump your classifier, dataset, and features_list so anyone can      ###
### check your results. You do not need to change anything below, but make sure ###
### that the version of poi_id.py that you submit can be run on its own and     ###
### generates the necessary .pkl files for validating your results.             ###
###################################################################################

dump_classifier_and_data(clf, my_dataset, features_list)