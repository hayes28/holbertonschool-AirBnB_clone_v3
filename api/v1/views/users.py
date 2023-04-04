#!/usr/bin/python3
"""View for user objects, handles default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, Flask, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_users(user_id=None):
    """Retrieves all users, by id"""
    users = storage.all(User)

    if request.method == 'GET':
        if user_id is None:
            return jsonify([user.to_dict() for user in users.values()])

        selected = storage.get(User, user_id)
        if selected is None:
            abort(404)
        return jsonify(selected.to_dict())

    elif request.method == 'POST':
        user_data = request.get_json()
        if not user_data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'email' not in user_data:
            return make_response(jsonify({'error': 'Missing email'}), 400)
        if 'password' not in user_data:
            return make_response(jsonify({'error': 'Missing password'}), 400)
        user_add = User(**user_data)
        storage.save()
        return make_response(jsonify(user_add.to_dict()), 201)

    elif request.method == 'DELETE':
        userdelete = storage.get(User, user_id)
        if userdelete is None:
            abort(404)
        storage.delete(userdelete)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        user_update = storage.get(User, user_id)
        if user_update is None:
            abort(404)
        if request.is_json:
            user_data = request.get_json()
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, val in user_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(user_update, key, val)
        storage.save()
        return make_response(jsonify(user_update.to_dict()), 200)
