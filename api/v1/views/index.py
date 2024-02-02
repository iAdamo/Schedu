#!/usr/bin/python3
""" Index file for api/v1
"""

from api.v1.views import app_views
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return status """
    return {"status": "OK"}


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves the number of each objects by type
    """
    objects = {
        "Teacher": Teacher,
        "Student": Student,
        "Guardian": Guardian,
        "Admin": Admin}
    return jsonify({key: storage.count(obj) for key, obj in objects.items()})
