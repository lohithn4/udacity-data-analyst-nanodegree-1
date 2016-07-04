# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import unicodedata

from bs4 import BeautifulSoup
html_page = "postzones.html"

"""
This code will wrangle the data and transform the shape of the data
into the model defined. The output should be a list of dictionaries
in a json file
"""


# Phone numbers should be formated like this: +58-212-xxxxxxx
# House numbers should be numerical only    
# Post codes should be a 4 digit number
numerical_re = re.compile(r'^-?[0-9]+$')
postal_re = re.compile(r'^[0-9]{4}$')
phone_re = re.compile(r'^\+?\d{1,2}?[-]?\d{1,3}?[-]?\d\d\d\d\d\d\d$')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
ADDRESS = ["housenumber", "housename", "street", "postcode"]
OTHER   = ["id", "name", "amenity", "cuisine", "shop", "phone"]

# street
street_type_re = re.compile(r'Av\.|Av', re.IGNORECASE)
STREET = ["Avenida"]
mapping = {"Av." : "Avenida", "Av" : "Avenida", "av" : "Avenida"}


'''
Validation and data cleaning functions
'''

def validate_re(re, string):
    if re.search(string):
        return True
    return False


def fix_street(street_string):
    # Street abbreviations should be changed to follow this mapping: 
    match = street_type_re.search(street_string)
    if match:
        street_type = match.group()
        if street_type not in STREET:
            street_string = re.sub(street_type_re, mapping[street_type], street_string)

    return street_string

'''
Data improvement mapping of post codes to respective post zones
'''

def extract_postzones(page):
    
    data = {}

    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")
        
        table = soup.find(id='postzones')
        rows = table.find_all('tr')
        
        for r in rows:
            cols = r.find_all('td')

            zone = cols[0].text
            code = cols[2].text[1:] # removing first char because its a 0
            
            if code in data:
                data[code].append(zone)
            else:
                data[code] = []
                data[code].append(zone)
    
    return data      


'''
This function shapes the data into the model defined
'''

def shape_element(element, postzones):
    
    node = {}
    
    if element.tag == "node" or element.tag == "way" :
        
        node['created'] = {}
        node['type'] = element.tag
        node['address'] = {}
        remove_address = 'yes'

        if element.tag == "node":
            node['pos'] = [0.0,0.0]
            
        if element.tag == 'way':
                node['node_refs'] = []
            
        # top level
        attributes = element.attrib
        for k,v in attributes.items():    
            # created
            if k in CREATED:
                node['created'][k] = v
            # pos
            elif k in ['lat', 'lon']:
                if k == 'lat':
                    node['pos'][0] = float(v)
                else:
                    node['pos'][1] = float(v)
            #id
            elif k == 'id':
                node[k] = v
               
        # check sub-tags: "tag" for node and "nd" for way
        for item in element:
            attributes = item.attrib
            if item.tag == 'nd':
                node['node_refs'].append(attributes['ref'])
            else:
                k = attributes['k']
                v = attributes['v']
                # if two ":", ignore
                if k.count(":") > 1:
                    continue
                # if address
                if k.startswith('addr:'):
                    remove_address = 'no'
                    address_key = k.split(':')[1]
                    
                    if address_key in ADDRESS:
                        if address_key == "housenumber":
                            if validate_re(numerical_re,v):
                                node['address'][address_key] = v
                        elif address_key == "postcode":
                            if validate_re(postal_re,v): 
                                node['address'][address_key] = v
                                
                                # add postzones
                                if v in postzones:
                                    node['postzone'] = postzones[v]
                                
                        elif address_key == "street":
                            node['address'][address_key] = fix_street(v)
                        else: # housename
                            node['address'][address_key] = v
                # other tag attributes
                elif k in OTHER:
                    if k == "phone":
                        if validate_re(phone_re,v):
                            node[k] = v
                    else:
                        node[k] = v
                    
        if remove_address == 'yes':
            del node['address']
        
        '''
        print 'type: ' +element.tag
        pprint.pprint(node)
        print "========="
        '''
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):

    file_out = "caracas_venezuela.json"
    data = []
    
    postzones = extract_postzones(html_page)
    
    with codecs.open(file_out, "w", encoding="utf-8") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element, postzones)
            
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2, ensure_ascii=False)+"\n")
                else:
                    fo.write(json.dumps(el, ensure_ascii=False) + "\n")
            
    return data

def main():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('caracas_venezuela.osm')
    #pprint.pprint(data[-1])
    

if __name__ == "__main__": main()