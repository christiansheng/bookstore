# -*- coding: UTF-8 -*-
import os
import uuid
import time
import datetime
from pprint import pprint
from flask import jsonify
from flask import request
from flask import abort
from flask import current_app
import elasticsearch
from bson import ObjectId
import time
import pymongo
from pprint import pprint
import random

class MongoInstance:
    db = None
    client = None

    def __init__(self, db_name):
        for tryCount in range(0, 5):
            try:
                # Todo ^sheng :should not hard coding ("localhost", 27017)
                client = pymongo.MongoClient()
                print("MongoClient OK")
                break
            except Exception as ex:
                print('exception when trying to connect to MongoDB: %s' % ex)
                time.sleep(10)
        self.client = client
        self.db = client[db_name]

    def get_db(self):
        if self.db is not None:
            return self.db
        else:
            print("DB not initialised!")

    def close(self):
        self.client.close()
        self.db = None
        self.client = None


try:
    mongo_instance = MongoInstance('bookstore')
    db = mongo_instance.get_db()
    result = db.books.find()
    books = [book for book in result]
    for book in books:
        book['_id'] = str(book['_id'])
    # pprint(books)
    mongo_instance.close()
except Exception as ex:
    print(ex)
    mongo_instance.close()

press_id = {
    '电子工业出版社': 0,
    '清华大学出版社': 1,
    '人民邮电出版社': 2,
    '机械工业出版社': 3,
    'Apress': 4,
    "O'Reilly": 5,
    'Packt': 6
}

es = elasticsearch.Elasticsearch()
index_name = "bookstore"
type_name = "books"
try:
    for book in books:
        book['year'] = 2000 + int(random.random()*15)
        book['press_id'] = press_id[book['press']]
        print(book)
        es.index(index=index_name, doc_type=type_name, id=book['_id'], body=book)
except Exception as ex:
    print(ex)
