# -*- coding: utf-8 -*-
import os
import pymongo
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():

    # Docker will set the address of the linked MongoDB container in the following
    # environmental variable.  We already know the port that MongoDB is exposed on.
    db_host = str(os.environ["DB_PORT_27017_TCP_ADDR"])
    db_port = 27017

    # Get a connection to MongoDB, then get the collection 'webStats' from the
    # database 'app2Db'.
    client = pymongo.MongoClient(db_host, db_port)
    collection = client["app2Db"]["webStats"]

    # Increment the hit count for the page 'home' by one.
    collection.update({"_id":"home"},{"$inc":{"hit_count":1}}, True)

    # Read the value of the hit counter
    hit_count = collection.find_one({"_id":"home"})["hit_count"]

    return """<h1>This is app2!</h1>
              <p>Hit Count: %d </p>
              <img src='/static/images/flask-badge-2.png'/>""" % (hit_count)


if __name__ == '__main__':
    app.run() 