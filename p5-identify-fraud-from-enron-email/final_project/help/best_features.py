#!/usr/bin/python

import pickle
import sys
sys.path.append("../../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

from sklearn.feature_selection import SelectKBest

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

features_list = ['poi'] + financial_features + email_features

with open("../final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    

outliers = ["TOTAL", "THE TRAVEL AGENCY IN THE PARK"]
for o in outliers:
    data_dict.pop(o,0)

########################        
### Add new features ###
########################
    
# ratio_to_poi   = from_this_person_to_poi / to_messages
# ratio_from_poi = from_poi_to_this_person / from_messages
my_new_features = ["ratio_to_poi", "ratio_from_poi"]
features_list += my_new_features

       
for item in data_dict:
    person = data_dict[item]
    
    # New feature 1: ratio_to_poi
    #---------------------------
    if person["from_this_person_to_poi"] == 'NaN' or person["to_messages"] == 'NaN':
        person["ratio_to_poi"] = 'NaN'
    else:
        person["ratio_to_poi"] = float(person["from_this_person_to_poi"]) / float(person["to_messages"])
    
    # New feature 2: ratio_from_poi
    #---------------------------
    if person["from_poi_to_this_person"] == 'NaN' or person["from_messages"] == 'NaN':
        person["ratio_from_poi"] = 'NaN'
    else:
        person["ratio_from_poi"] = float(person["from_poi_to_this_person"]) / float(person["from_messages"])
    
#######################################        
### Best features using SelectKBest ###
#######################################
    
data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

k = 15
kbest = SelectKBest(k=k)
kbest.fit(features, labels)

scores = kbest.scores_
unsorted = zip(features_list[1:], scores)
features_scores = list(reversed(sorted(unsorted, key=lambda x: x[1])))

for f, s in features_scores[:k]:
    print f,": ", s
    
    