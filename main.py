
from google.cloud import datastore
from flask import Flask, request
import json
import constants
import boat
import load

app = Flask(__name__)
app.register_blueprint(boat.bp)
app.register_blueprint(load.bp)
client = datastore.Client()

@app.route('/')
def index():
    return "Please navigate to /lodgings to use this API"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


