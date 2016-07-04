# -*- coding: utf-8 -*-

import pprint

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def aggregate(db, pipeline):
    return [doc for doc in db.caracas.aggregate(pipeline)]

def totals(db):
    print 'Documents: {}'.format(db.caracas.find().count())
    print 'Nodes: {}'.format(db.caracas.find({'type':'node'}).count())
    print 'Ways: {}'.format(db.caracas.find({'type':'way'}).count())
    print 'Unique Users: {}'.format(len(db.caracas.distinct("created.user")))

def top_users(db):

    pipeline = [
        {"$group" : {"_id" : "$created.user",
                     "count" : {"$sum" : 1} } },
        {"$sort" : {"count": -1} },
        {"$limit" : 10}
    ]
    
    result = aggregate(db, pipeline)    
    print 'Top Users:'    
    pprint.pprint(result)

def bottom_users(db):

    pipeline = [
        {"$group" : {"_id" : "$created.user",
                     "count" : {"$sum" : 1} } },
        {"$match" : {"count" : {"$lte" : 2} } },
        {"$group" : { "_id": None, "count" : {"$sum" : 1 } } },
    ]
    
    result = aggregate(db, pipeline)         
    print 'Number of Bottom Users:'
    pprint.pprint(result)

def top_amenities(db):
    
    pipeline = [
        {"$match" : {"amenity" : {"$exists" : 1} } },
        {"$group" : {"_id" : "$amenity",
                     "count" : {"$sum" : 1} } },
        {"$sort" : {"count": -1} },
        {"$limit" : 10}
    ]
    
    result = aggregate(db, pipeline)    
    print 'Top Amenities:'    
    pprint.pprint(result)

def top_shops(db):
    
    pipeline = [
        {"$match" : {"shop" : {"$exists" : 1} } },
        {"$group" : {"_id" : "$shop",
                     "count" : {"$sum" : 1} } },
        {"$sort" : {"count": -1} },
        {"$limit" : 10}
    ]
    
    result = aggregate(db, pipeline)    
    print 'Top Shops:'    
    pprint.pprint(result)    
    
def no_address(db):
    
    pipeline = [
        {"$match" : {"type" : "node",
                     "address" : {"$exists" : 0} } }, 
        {"$group" : {"_id" : None,
                    "count" : {"$sum": 1} } }
    ]
    
    result = aggregate(db, pipeline)    
    print 'Nodes without address:'    
    pprint.pprint(result) 
    

if __name__ == '__main__':
    
    db = get_db('udacity')
    
    totals(db)
    
    print '-----------------------------------------'    
           
    top_users(db)
    
    print '-----------------------------------------'

    bottom_users(db)
    
    print '-----------------------------------------'
    
    top_amenities(db)
    
    print '-----------------------------------------'
    
    top_shops(db)
    
    print '-----------------------------------------'
    
    no_address(db)
    
    
    
    
    
    