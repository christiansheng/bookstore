import pymongo
from bson.objectid import ObjectId
from pprint import pprint
from bson.json_util import dumps
from json import loads, load

client = pymongo.MongoClient()
db = client.bookstore
