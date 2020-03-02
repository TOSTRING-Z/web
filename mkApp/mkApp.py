from flask import Flask, request
from flask import jsonify

import py.sql as pysql

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
    app.run(host='127.0.0.1', port=5001, debug=True)
