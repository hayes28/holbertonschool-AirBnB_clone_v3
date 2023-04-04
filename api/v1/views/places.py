#!/usr/bin/python3
"""View for place objects; handles defualt RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=[
    'GET'], strict_slashes=False)
def get_places(city_id=None):
    """retrieves all places associated with city id"""
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city is None:
            abort(404)
        return jsonify([places.to_dict() for places in city.places])


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_get_or_delete(place_id=None):
    """Retrieves a place or deletes a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        if request.is_json:
            place_data = request.get_json()
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        ignore_list = ['id', 'created_at', 'updated_at', 'city_id']
        for key, val in place_data.items():
            if key not in ignore_list:
                setattr(place, key, val)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id=None):
    """creates a place"""
    place_data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not place_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in place_data.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if storage.get(User, place_data['user_id']) is None:
        abort(404)
    if 'name' not in place_data.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_place = Place(**place_data)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)
