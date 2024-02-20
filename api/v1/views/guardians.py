#!/usr/bin/python3
"""Guardian view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.guardian import Guardian
from flask_jwt_extended import jwt_required


@app_views.route('/guardians', strict_slashes=False)
@jwt_required()
def guardians():
    """returns a list of all guardians
    """
    return jsonify([guardian.to_dict()
                   for guardian in storage.all(Guardian).values()])


@app_views.route('/guardians/<guardian_id>', strict_slashes=False)
@jwt_required()
def guardian(guardian_id):
    """returns a guardian object by id
    """
    guardian = storage.get(Guardian, guardian_id)
    if guardian is None:
        abort(404)
    return guardian.to_dict()


@app_views.route('/guardians/<guardian_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@jwt_required()
def delete_guardian(guardian_id):
    """deletes a guardian object by id
    """
    guardian = storage.get(Guardian, guardian_id)
    if guardian is None:
        abort(404)
    guardian.delete()
    storage.save()
    return {}, 200


@app_views.route('/guardians', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_guardian():
    """creates a guardian object
    """
    guardian = request.get_json()
    if guardian is None:
        abort(400, "Not a JSON")
    if "name" not in guardian:
        abort(400, "Missing name")
    guardian = Guardian(**guardian)
    guardian.save()
    return guardian.to_dict(), 201


@app_views.route('/guardians/<guardian_id>',
                 methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_guardian(guardian_id):
    """updates a guardian object
    """
    guardian = storage.get(Guardian, guardian_id)
    if guardian is None:
        abort(404)
    update = request.get_json()
    if update is None:
        abort(400, "Not a JSON")
    for key, value in update.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(guardian, key, value)
    guardian.save()
    return guardian.to_dict(), 200
