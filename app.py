from flask import Flask, jsonify, request
import json
from random import randint
from datetime import date

app = Flask(__name__)

MAX_REWARD = 20

data = {}

with open("data.json") as file:
    data = json.loads(file.read())

print(data['parlors'])


# Functions
def playMachine(mid, gid, uid):

    for i, m in enumerate(data['machines']):
        if mid == m['id']:

            if m['status'] == 'occupied':
                return jsonify({'ERROR': 'MACHINE OCCUPIED'})

            amount = getGamPrice(mid, gid)
            print(amount)
            if isNotPlayable(uid, amount):
                return({'ERROR': 'INSUFFICIENT BALANCE'})

            addMoney(uid, -amount)

            data['machines'][i]['status'] = 'occupied'

            t = {
                "id": "t"+str(len(data['transactions'])+1),
                "type": "game",
                "itemId": gid,
                "amount": amount,
                "pid": getParlorID(mid),
                "uid": uid,
                "mid": mid
            }
            #addEarnings(getParlorID(mid), amount)

            data['transactions'].append(t)

            return jsonify({'machine': data['machines'][i], 'transaction': t})

    return jsonify({'ERROR': 'NOT FOUND'})


def stopMachine(mid, uid):

    for i, m in enumerate(data['machines']):
        if mid == m['id']:
            data['machines'][i]['status'] = 'available'
            reward = randint(0, MAX_REWARD)
            addMoney(uid, reward)
            return jsonify({'machine': data['machines'][i], 'reward': reward})

    return jsonify({'ERROR': 'NOT FOUND'})


def addMoney(uid, amount):
    for i, u in enumerate(data['users']):
        if uid == u['id']:
            data['users'][i]['card']['amount'] += amount


def getGamPrice(mid, gid):
    for i, m in enumerate(data['machines']):
        if mid == m['id']:
            for i, g in enumerate(m['games']):
                if gid == g['id']:
                    return g['price']
    return -1


def isNotPlayable(uid, amount):
    today = str(date.today())
    # print("Today's date:", today)
    if amount < 0:
        return True
    else:
        for u in data['users']:
            if uid == u['id']:
                if u['card']['daily'] == today:
                    return False
                elif u['card']['amount'] > amount:
                    return False

    return True


def getParlorID(mid):
    return 'p1'
# Routes


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
    uid = request.json["uid"]

    return playMachine(mid, game_id, uid)


@app.route('/machine/<mid>/stop', methods=['POST'])
def machine_stop(mid):
    """
    Return the Random reward as well
    """
    uid = request.json["uid"]

    return stopMachine(mid, uid)


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


# Transactions
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
