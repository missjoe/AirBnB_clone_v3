#!/usr/bin/python3
""" New views for amenities """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
import models


@app_views.route('/amenities', methods=['GET'])
def showAmenities():
    """ Shows all amenitiess db storage """
    myList = []
    for value in models.storage.all("Amenity").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def showAmenityId(amenity_id):
    """ Shows a specific amenity in db storage """
    amenity = models.storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def deleteAmneityId(amenity_id):
    """ Deletes a amenity in db storage """
    amenity = models.storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'])
def createAmenity():
    """ Creates a amenity db storage """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    amenity = Amenity(**content)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def putAmenity(amenity_id):
    """ Updates an Amenity in db storage """
    amenity = models.storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
