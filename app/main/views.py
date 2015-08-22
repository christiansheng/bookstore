# -*- coding: UTF-8 -*-
from flask import request
from flask import jsonify
from pprint import pprint
from flask import render_template, abort
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



# just for test purpose
@main.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.json
        print(data)
        for x in data:
            print(x)
        return 'post ok'
        pass