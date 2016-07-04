#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

# size
print len(enron_data)

# number of features
print len(enron_data["SKILLING JEFFREY K"])

# total PoIs
pois = 0
for name, features in enron_data.iteritems():
    if(features["poi"]):
        pois = pois + 1
print pois

# stock value of James Prentice
print enron_data["PRENTICE JAMES"]["total_stock_value"]

# emails from Wesley Colwell to PoI
print enron_data["COLWELL WESLEY"]["from_this_person_to_poi"]

# value of stock options exercised by Jeffrey Skilling
print enron_data["SKILLING JEFFREY K"]["exercised_stock_options"]


# who tool most total payments
print enron_data["LAY KENNETH L"]["total_payments"]
print enron_data["SKILLING JEFFREY K"]["total_payments"]
print enron_data["FASTOW ANDREW S"]["total_payments"]

# How many have a quantified salary? How many have a known email address?
have_salary = 0
have_email = 0
for name, features in enron_data.iteritems():
    if(features["salary"] != 'NaN'):
        have_salary = have_salary + 1
    if(features["email_address"] != 'NaN'):
        have_email = have_email + 1
print have_salary
print have_email

# How many people in the E+F dataset (as it currently exists) have 'Nan' for their total payments? 
# What percentage of people in the dataset as a whole is this?
no_payment = 0
for name, features in enron_data.iteritems():
    if(features["total_payments"] == 'NaN'):
        no_payment = no_payment + 1
print float(no_payment)/float(len(enron_data))
print no_payment

# How many POIs in the E+F dataset have 'NaN' for their total payments? 
# What percentage of POI's as a whole is this?
no_payment = 0
for name, features in enron_data.iteritems():
    if(features["poi"]):    
        if(features["total_payments"] == 'NaN'):
            no_payment = no_payment + 1
print float(no_payment)/float(len(enron_data))
