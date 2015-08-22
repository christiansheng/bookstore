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
from ..models.mongo import MongoInstance
from . import api
from bson.json_util import dumps
import uuid
from json import loads

# done & tested
# Route that will process the file upload
@api.route('/upload', methods=['POST'])
def upload():

    name = str(request.form.get("name", None))
    press_number = int(request.form.get("press", None))
    author = str(request.form.get("author", None))
    keywords = str(request.form.get("keywords", None))
    brief = str(request.form.get("brief", None))

    press = [
        '电子工业出版社',
        '清华大学出版社',
        '人民邮电出版社',
        '机械工业出版社',
        'Apress',
        "O'Reilly",
        'Packt'
    ]
    lang = "CN"
    if press_number > 3:
        lang = 'EN'
    author = author.split(' ')
    keywords = keywords.split(' ')
    book = {
        # '_id': uuid.uuid4(),
        'name': name,
        'press': press[press_number],
        'language': lang,
        'author': author,
        'brief': brief,
        'keywords': keywords,
        'create_time': datetime.datetime.now()
    }

    print(book)
    try:
        mongo_instance = MongoInstance('bookstore')
        db = mongo_instance.get_db()
        books = db.books
        books.insert(book)
        mongo_instance.close()
    except Exception as ex:
        print(ex)
        mongo_instance.close()
        return jsonify({'result': False}), 500



    #  Todo: do not forget to delete filecount and filenames in production release. it is just for test usage.
    return jsonify(loads(dumps({'result': True, 'data': book})))


