import json
from bson.objectid import ObjectId
from bson.json_util import dumps

import pymongo
from pprint import pprint

import datetime
from bson import json_util

def json_dump_handler(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def getMongoDB(db_name):
    for tryCount in range(0, 5):
        try:
            # Todo ^sheng :should not hard coding ("localhost", 27017)
            client = pymongo.MongoClient("localhost", 27017)
            print("MongoClient OK")
            break
        except Exception as ex:
            print('exception when trying to connect to MongoDB: %s' % ex)
    return client[db_name]

global_id = "55cc4fc25e370e279cb8d425"
db = getMongoDB("xxx")
#db.profiles.update_one({"GlobalIdentity": ObjectId(global_id)}, {'$set': {"IsDeleted": True}})
r = db.profiles.find_one({"GlobalIdentity": ObjectId(global_id)})
print(r)
type_r = type(r)
print(type_r)
print(dumps(r))
print(json.dumps(r, default=json_util.default))