#!/usr/bin/python3
""" New views for cities """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
import models


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'])
def showCities(state_id):
    """ Shows all cities for a state in db storage """
    state = models.storage.get("State", state_id)
    if state:
        citiesList = []
        eachCity = models.storage.all("City")
        for value in eachCity.values():
            if value.state_id == state_id:
                citiesList.append(value.to_dict())
        return jsonify(citiesList)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def showCity(city_id):
    """ Shows a specific city in db """
    city = models.storage.get("City", city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deleteCity(city_id):
    """ Deletes a city in db storage """
    city = models.storage.get("City", city_id)
    if city:
        city.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def createCity(state_id):
    """ Creates a city for a state in db storage """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    if models.storage.get("State", state_id) is None:
        abort(404)
    data = request.get_json()
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updateCity(city_id):
    """ Updates a city in db storage """
    city = models.storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
