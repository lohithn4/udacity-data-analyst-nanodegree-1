# -*- coding: utf-8 -*-

"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

import xml.etree.cElementTree as ET
import pprint
import operator

def process_map(filename):
    users = {}
    uids = {}
    for _, element in ET.iterparse(filename):
        if element.tag == "node" or element.tag == "way" :        
            user = element.get("user")
            uid = element.get("uid")
            if user in users:
                users[user] += 1
            else:
                users[user] = 1
            
            if uid in uids:
                uids[uid] += 1
            else:
                uids[uid] = 1
            
    return users, uids


def main():

    users, uids = process_map('caracas_venezuela.osm')
    print "Total unique users: {}".format(len(users))
    #print "Total unique uids: {}".format(len(uids))
    #pprint.pprint(users)
    
    sorted_users = sorted(users.items(), key=operator.itemgetter(1))
    pprint.pprint(sorted_users)

if __name__ == "__main__": main()
    