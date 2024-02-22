#!/usr/bin/python3
""" Index file for api/v1
"""

from flask_jwt_extended import get_jwt_identity, jwt_required
from api.v1.views import app_views
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian
from flask import jsonify, request
from models import storage
from flask import abort, jsonify, request

objects = {
    "Teacher": Teacher,
    "Student": Student,
    "Guardian": Guardian,
    "Admin": Admin
}


@app_views.route('/data', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_data():
    current_user = get_jwt_identity()

    data = {
        'user': {'info': 'Data for user'},
        'admin': {'info': 'Data for admin'}
    }

    user_data = data.get(
        current_user, {
            'info': 'No data available for this user'})
    return jsonify(user_data)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Return the status of the API """
    current_user = get_jwt_identity()
    return jsonify({"status": "OK", "user": current_user})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Retrieves the number of each object by type """
    return jsonify({key: storage.count(obj) for key, obj in objects.items()})


@app_views.route('/search/<char>', strict_slashes=False)
def search(char):
    """searches for a specific value in the database
    
    curl -X POST -H "Content-Type: application/json" -H "Authorization:
    Bearer " -d '{"first_name": "A"}' http://localhost:5001/api/v1/search
    """
    # currently every user can search for every other user
    # this should be changed to only the admins being able to search for everyone
    # if not current_user.is_admin:
    #     return jsonify({"error": "Unauthorized"}), 401
    results = []
    for obj in storage.all().values():
        obj_dict = obj.to_dict()
        if 'name' in obj_dict and char.lower() in obj_dict['name'].lower():
            results.append({'id': obj_dict['id'], 'name': obj_dict['name']})
    return jsonify(results)

@app_views.route('/profile/<userid>', strict_slashes=False)
def profiles(userid):
    """ Retrieve users by id """
    user = storage.all().values()
    for obj_dict in user:
        if obj_dict.id == userid:
            return jsonify(obj_dict.to_dict())
    return jsonify({"error": "Not found"}), 404
