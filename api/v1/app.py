#!/usr/bin/python3
""" This module create an API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv, environ
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def handleclose(self):
    """ method to close database session """
    storage.close()


@app.errorhandler(404)
def errorhand(e):
    """ Return JSON instead of HTML """
    data = {"error": "Not found"}
    return (jsonify(data), 404)


if __name__ == '__main__':
    app.run(host=getenv("HBNB_API_HOST"), port=getenv("HBNB_API_PORT"),
            threaded=True)
