#!/usr/bin/python3
"""Views for ammentities objects: handles Resftul API methods"""

from api.v1.views import app_views
from flask import jsonify, request, abort, Flask, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(state_id=None):
    """retrieves all states, by id"""
    amenities = storage.all(Amenity)

    if request.method == 'GET':
        if state_id is None:
            return jsonify([amenity.to_dict()
                            for amenity in amenities.values()])


@app_views.route('/amenities', methods={'POST'}, strict_slashes=False)
def create_amenity():
    """creates a new amenity object"""
    amenity_data = request.get_json()
    if amenity_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in amenity_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**amenity_data)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """gets a single amenity object based on ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """deletes a single amenity object based on id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in post_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
