from flask import Flask, jsonify, request
from todx import fabric
import json
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    with open('data.json') as file:
        return file.read()

@app.route('/hash', methods = ['POST'])
def hash():
    """
    Requires a request of the format:
    {
            'hash' : 'HASH'
    }
    and returns whether the file has changed or not
    """
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        print(type(data))
        with open('data.json') as dataFile:
            readfile = dataFile.read().encode('utf8')
            md5Hash = hashlib.md5(readfile)
            md5Hashed = md5Hash.hexdigest()
            print(md5Hashed)
            if data['hash'] == md5Hashed:
                return jsonify(
                    {
                        'status':'matched'
                    }
                )
            else:
                return jsonify(
                    {
                        'status':'changed'
                    }
                )

if __name__ == '__main__':
    app.run()