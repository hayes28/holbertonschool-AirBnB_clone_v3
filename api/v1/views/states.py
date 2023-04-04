#!/usr/bin/python3
"""View for state objects; handles defualt RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, Flask, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_states(state_id=None):
    """retrieves all states, by id"""
    states = storage.all(State)

    if request.method == 'GET':
        if state_id is None:
            return jsonify([state.to_dict() for state in states.values()])

        selected = storage.get(State, state_id)
        if selected is None:
            abort(404)
        return jsonify(selected.to_dict())

    elif request.method == 'POST':
        state_data = request.get_json()
        if not state_data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in state_data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        state_add = State(**state_data)
        storage.save()
        return make_response(jsonify(state_add.to_dict()), 201)

    elif request.method == 'DELETE':
        statedelete = storage.get(State, state_id)
        if statedelete is None:
            abort(404)
        storage.delete(statedelete)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        state_update = storage.get(State, state_id)
        if state_update is None:
            abort(404)
        if request.is_json:
            state_data = request.get_json()
        else:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, val in state_data.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state_update, key, val)
        storage.save()
        return make_response(jsonify(state_update.to_dict()), 200)
