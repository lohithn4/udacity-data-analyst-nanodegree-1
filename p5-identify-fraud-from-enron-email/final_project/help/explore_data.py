#!/usr/bin/python

import pickle

### Load the dictionary containing the dataset
with open("../final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

#######################
### Explore dataset ###
#######################

# Size

print "Dataset size: ", len(data_dict)

# Number of features

print "Number of features: ", len(data_dict["SKILLING JEFFREY K"])

# Number of POIs

poi_count = 0

for name, features in data_dict.iteritems():
    if(features["poi"]):
        poi_count = poi_count + 1
print "POIs in the dataset: ", poi_count
