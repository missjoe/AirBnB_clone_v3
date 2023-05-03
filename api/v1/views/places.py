#!/usr/bin/python3
""" New views for cities """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
import models


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'])
def showPlaces(city_id):
    """ Shows all places for a city in db storage """
    city = models.storage.get("City", city_id)
    if city:
        placesList = []
        eachPlace = models.storage.all("Place")
        for value in eachPlace.values():
            if value.city_id == city_id:
                placesList.append(value.to_dict())
        return jsonify(placesList)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def showPlace(place_id):
    """ Shows a specific place in db """
    place = models.storage.get("Place", place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def deletePlace(place_id):
    """ Deletes a place in db storage """
    place = models.storage.get("Place", place_id)
    if place:
        place.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def createPlace(city_id):
    """ Creates a place for a city in db storage """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    if models.storage.get("City", city_id) is None:
        abort(404)

    data = request.get_json()
    if models.storage.get("User", data["user_id"]) is None:
        abort(404)
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def updatePlace(place_id):
    """ Updates a city in db storage """
    place = models.storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200
