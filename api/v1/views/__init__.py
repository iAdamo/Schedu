#!/usr/bin/python3
""" Init file for api/v1
"""
from flask_jwt_extended import create_access_token
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.admins import *
from api.v1.views.teachers import *
from api.v1.views.students import *
from api.v1.views.guardians import *


# Define users (for demonstration purposes)
users = {
    'admin': 'admin',
    'user': 'password'
}

# User login endpoint
@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
