#!/usr/bin/python3
""" New views for Reviews """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
import models


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET'])
def showReviews(place_id):
    """ Shows all reviews for a place in db storage """
    place = models.storage.get("Place", place_id)
    if place:
        reviewsList = []
        eachReview = models.storage.all("Review")
        for value in eachReview.values():
            if value.place_id == place_id:
                reviewsList.append(value.to_dict())
        return jsonify(reviewsList)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def showReview(review_id):
    """ Shows a specific review in db """
    review = models.storage.get("Review", review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def deleteReview(review_id):
    """ Deletes a review in db storage """
    review = models.storage.get("Review", review_id)
    if review:
        review.delete()
        models.storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def createReview(place_id):
    """ Creates a review for a place in db storage """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in request.json:
        return jsonify({"error": "Missing text"}), 400
    if models.storage.get("Place", place_id) is None:
        abort(404)

    data = request.get_json()
    if models.storage.get("User", data["user_id"]) is None:
        abort(404)
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def updateReview(review_id):
    """ Updates a review in db storage """
    review = models.storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    for key, val in request.get_json().items():
        if key not in [
            'id',
            'created_at',
            'updated_at',
            'user_id',
                'place_id']:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200
