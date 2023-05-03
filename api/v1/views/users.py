#!/usr/bin/python3
""" New views for users """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
import models


@app_views.route('/users', methods=['GET'])
def showUsers():
    """ Shows all users db storage """
    myList = []
    for value in models.storage.all("User").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/users/<user_id>', methods=['GET'])
def showUserbyId(user_id):
    """ Shows a specific user in db storage """
    user = models.storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    """ Deletes an user in db storage """
    user = models.storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'])
def createUser():
    """ Creates an user db storage """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400

    data = request.get_json()
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def putUser(user_id):
    """ Updates an User in db storage """
    user = models.storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
