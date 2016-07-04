# -*- coding: utf-8 -*-

"""
Parse data and get a sample of values for each key to get insight on data
quality and consistency. Will export results to a json file
"""

import xml.etree.cElementTree as ET
import json


'''
Based on the defined data model
'''
unique_keys_dict = {
    "addr:housenumber" : [],
    "addr:housename" : [],
    "addr:street" : [],
    "addr:postcode" : [],
    "name" : [],
    "amenity" : [],
    "cuisine" : [],
    "shop" : [],
    "phone" : []
}
                       

'''
This function will add the values to the dict. Since there are so many tags,
only a sample will be added
'''

def add_value_to_dict(element):
    sample_size = 100
    if element.tag == "tag":
        k = element.attrib['k']
        v = element.attrib['v']
        if k in unique_keys_dict:        
            if(len(unique_keys_dict[k]) <= sample_size):
                # avoid duplicates                
                if v not in unique_keys_dict[k]:         
                    unique_keys_dict[k].append(v)


'''
This function will parse the data and create the json file with the values of 
the keys
'''

def main():
    
    filename = 'caracas_venezuela.osm' 
       
    for _, element in ET.iterparse(filename):
        add_value_to_dict(element)

    json.dump(unique_keys_dict, open('keys-data.json', 'w'))
    
    
    
if __name__ == "__main__": main()