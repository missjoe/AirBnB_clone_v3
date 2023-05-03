#!/usr/bin/python3
""" New view for states """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
import models


@app_views.route('/states', methods=['GET'])
def showStates():
    """ Shows all states db storage """
    myList = []
    for value in models.storage.all("State").values():
        myList.append(value.to_dict())
    return jsonify(myList)


@app_views.route('/states/<state_id>', methods=['GET'])
def showStateId(state_id):
    """ Shows all states db storage """
    state = models.storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleteStateId(state_id):
    """ Deletes a state in db storage """
    state = models.storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    models.storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'])
def createState():
    """ Creates a state db storage """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    content = request.get_json()
    state = State(**content)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def putStates(state_id):
    """ Updates a State in db storage """
    state = models.storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_dict()), 200
