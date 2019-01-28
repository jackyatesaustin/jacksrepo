from flask import Flask
from redis import Redis, RedisError
import os
import socket

# connect to redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

# home page
@app.route("/")
# basic hello world function
def hello():
    # try catch before opening then page so we don't shut down if DB is off
    try:
        #increment the redis counter
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    #basic flask-html and redis access
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

#create a new page /new to do some fun stuff
@app.route("/new")
def hellonew():

    # testing the build
    html = "<h3>Helloo, New: {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
