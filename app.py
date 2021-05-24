from flask import Flask, jsonify, request
import json
from random import randint

app = Flask(__name__)

MAX_REWARD = 20

data = {}

with open("data.json") as file:
    data = json.loads(file.read())

print(data['parlors'])


# Functions


@app.route('/', methods=['GET'])
def index():
    with open('data.json') as file:
        return file.read()


# Parlor Endpoints
@app.route('/parlor/<pid>', methods=['GET'])
def parlor_id(pid):
    """
    Return Parlor details by ID
    """
    for p in data['parlors']:
        if pid == p['id']:
            return jsonify(p)

    return jsonify(
        {
            'ERROR': 'NOT FOUND'
        }
    )


@app.route('/parlor/<pid>/transactions', methods=['GET'])
def parlor_transactions():
    """
    """
    return jsonify(
        {
            'status': 'changed'
        }
    )


# Machine Endpoints
@app.route('/machine/<mid>/', methods=['GET'])
def machine(mid):
    """
    Return Machine details
    """
    for m in data['machines']:
        if mid == m['id']:
            return jsonify(m)
    return jsonify(
        {
            'ERROR': 'NOT FOUND'
        }
    )


@app.route('/machine/<mid>/play/<game_id>', methods=['POST'])
def machine_play(mid, game_id):
    """
    Perform transaction, make machine occupied
    Fail with error
    """
    return jsonify(
        {
            'status': 'changed'
        }
    )


@app.route('/machine/<mid>/stop', methods=['POST'])
def machine_stop(mid):
    """
    Return the Random reward as well
    """
    for i, m in enumerate(data['machines']):
        if mid == m['id']:
            data['machines'][i]['status'] = 'available'

            return jsonify({'machine': data['machines'][i], 'reward': MAX_REWARD})

    return jsonify(
        {
            'status': 'changed'
        }
    )


# User Routes
@app.route('/user/<uid>/', methods=['GET'])
def user(uid):
    """
    Return User details
    """
    for u in data['users']:
        if uid == u['id']:
            return jsonify(u)
    return jsonify(
        {
            'ERROR': 'NOT FOUND'
        }
    )


@app.route('/user/<uid>/transactions', methods=['GET'])
def user_transactions(uid):
    """
    """
    return jsonify(
        {
            'status': 'changed'
        }
    )


@app.route('/user/<uid>/card', methods=['GET'])
def user_card(uid):
    """
    Current user card info
    """
    for u in data['users']:
        if uid == u['id']:
            return jsonify(u['card'])
    return jsonify(
        {
            'ERROR': 'NOT FOUND'
        }
    )


@app.route('/transaction/<tid>', methods=['GET'])
def transaction(tid):
    """
    Return User details
    """
    for t in data['transactions']:
        if tid == t['id']:
            return jsonify(t)
    return jsonify(
        {
            'ERROR': 'NOT FOUND'
        }
    )


@app.route('/transactions', methods=['GET'])
def transactions():
    """
    Return User details
    """
    return jsonify(data['transactions'])


if __name__ == '__main__':
    app.run()
