#!/usr/bin/python3
""" This module is a index page """

from api.v1.views import app_views
import models
from flask import jsonify


@app_views.route('/status')
def statuspage():
    """method to return status"""
    di = {"status": "OK"}
    return jsonify(di)


@app_views.route('/stats')
def statspage():
    """method to count the number of objects by type """
    di = {}
    di['amenities'] = models.storage.count("Amenity")
    di['cities'] = models.storage.count("City")
    di['places'] = models.storage.count("Place")
    di['reviews'] = models.storage.count("Review")
    di['states'] = models.storage.count("State")
    di['users'] = models.storage.count("User")
    return jsonify(di)
