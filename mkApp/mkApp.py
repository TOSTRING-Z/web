import requests
from flask import Flask, request, render_template, url_for, redirect, session, flash, Response, make_response
from functools import wraps
import py.sql as pysql
import json
from werkzeug.utils import secure_filename
import os
import re
import time
import random
from threading import Timer
from flask import jsonify

app = Flask(__name__)


@app.route('/app/home')
def appHome():
    start = request.values.get('start')
    result = pysql.appHome(start)
    if result:
        return jsonify(result)


@app.route('/app/search', methods=['GET'])
def appSearch():
    search = request.values.get('search')
    sort = request.values.get('sort')
    filter_arr = request.values.get('filter').split(',')
    start = request.values.get('start')
    result = pysql.appSearch(search, type, sort, filter_arr, start)
    if result:
        return jsonify(result)


@app.route('/app/video')
def appVideo():
    titleID = request.values.get('titleID')
    result = pysql.appVideo(titleID)
    if result:
        return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001, debug=True)
