#!/usr/bin/python3
"""return the status of your API

run: curl -X POST -H "Content-Type: application/json" -d
'{"username": "user1", "password": "password1"}' http://localhost:5001/login
to genarate a token

run: curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5001/data
to access the protected endpoint
"""


import os
from flask import Flask, make_response, jsonify, request
from flask_jwt_extended import JWTManager
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
jwt = JWTManager(app)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle a JSON-formatted 404 status code response"""
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    MGT_API_HOST = getenv('MGT_API_HOST')
    MGT_API_PORT = getenv('MGT_API_PORT')
    app.run(host='127.0.0.1', port='5001', debug=True, threaded=True)
