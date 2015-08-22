import pymongo
import time
from flask import current_app


class MongoInstance:
    db = None
    client = None

    def __init__(self, db_name):
        for tryCount in range(0, 5):
            try:
                # Todo ^sheng :should not hard coding ("localhost", 27017)
                client = pymongo.MongoClient(**current_app.config['MONGODB_SETTINGS'])
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


