#!/usr/bin/python3
""" Status of your API """
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(close):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(debug=True, host=host, port=port, threaded=True)
