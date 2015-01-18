# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>This is app2!</h1> <img src='/static/images/flask-badge-2.png'/>"

if __name__ == '__main__':
    app.run() 