#!/usr/bin/python3
""" Init file for api/v1
"""

from datetime import datetime
from flask import make_response
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
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=0.55))
        response = make_response(jsonify({'message': 'Logged in'}), 200)
        response.set_cookie('access_token', access_token, httponly=True, secure=False, samesite='None')
        return response
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
