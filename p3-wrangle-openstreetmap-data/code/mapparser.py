# -*- coding: utf-8 -*-

"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.
"""

import xml.etree.cElementTree as ET
import pprint
import operator

def count_tags(filename):
        
        tree = ET.parse(filename)
        root = tree.getroot()

        all_descendants = list(root.iter())

        tags_dict = {}
        keys_dict = {}    
        
        for e in all_descendants:
            if e.tag == 'tag':
                if e.attrib['k'] in keys_dict:              
                    keys_dict[e.attrib['k']] += 1
                else:
                    keys_dict[e.attrib['k']] = 1
            
            if e.tag in tags_dict:
                tags_dict[e.tag] += 1
            else:
                tags_dict[e.tag] = 1

        return tags_dict, keys_dict
        
def main():
    tags, keys = count_tags('caracas_venezuela.osm')
    
    '''    
    To visualize tags used in the .osm file uncomment code below   
    '''
        
    #pprint.pprint(tags)
    
    '''    
    To visualize MOST frequent keys, uncomment code below   
    '''
    
    # sorted_keys = sorted(keys.items(), key=operator.itemgetter(1))
    # pprint.pprint(sorted_keys[-30:])
    
    '''    
    To visualize LEAST frequent keys, uncomment code below   
    '''
    
    sorted_keys = sorted(keys.items(), key=operator.itemgetter(1))
    pprint.pprint(sorted_keys[:1000])

if __name__ == "__main__": main()
    
