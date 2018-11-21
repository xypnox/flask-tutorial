from flask import Flask
# from todx import fabric
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

