#!/usr/bin/python3
""" Index file for api/v1
"""

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required)
from api.v1.views import app_views
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian
from flask import jsonify, request
from models import storage

# Define users (for demonstration purposes)
users = {
    'miguel': 'python',
    'user1': 'password1',
    'user2': 'password2'
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

# Protected endpoint requiring JWT authentication


@app_views.route('/data', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_data():
    current_user = get_jwt_identity()

    data = {
        'user1': {'info': 'Data for user1'},
        'user2': {'info': 'Data for user2'},
        'miguel': {'info': 'Data for miguel'}
    }

    user_data = data.get(
        current_user, {
            'info': 'No data available for this user'})
    return jsonify(user_data)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
@jwt_required()
def status():
    """ Return the status of the API """
    current_user = get_jwt_identity()
    return jsonify({"status": "OK", "user": current_user})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
@jwt_required()
def stats():
    """ Retrieves the number of each object by type """
    current_user = get_jwt_identity()

    # You can customize the response or logic based on the authenticated user
    # if needed

    objects = {
        "Teacher": Teacher,
        "Student": Student,
        "Guardian": Guardian,
        "Admin": Admin
    }
    return jsonify({key: storage.count(obj) for key, obj in objects.items()})
