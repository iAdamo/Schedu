#!/usr/bin/python3
"""Admin view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.admin import Admin
from flask_jwt_extended import jwt_required


@app_views.route('/admins', strict_slashes=False)
@jwt_required()
def admins():
    """returns a list of all admins
    """
    return jsonify([admin.to_dict() for admin in storage.all(Admin).values()])


@app_views.route('/admins/<admin_id>', strict_slashes=False)
@jwt_required()
def admin(admin_id):
    """returns a admin object by id
    """
    admin = storage.get(Admin, admin_id)
    if admin is None:
        abort(404)
    return admin.to_dict()


@app_views.route('/admins/<admin_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@jwt_required()
def delete_admin(admin_id):
    """deletes a admin object by id
    """
    admin = storage.get(Admin, admin_id)
    if admin is None:
        abort(404)
    admin.delete()
    storage.save()
    return {}, 200


@app_views.route('/admins', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_admin():
    """creates a admin object
    """
    admin = request.get_json()
    if admin is None:
        abort(400, "Not a JSON")
    if "name" not in admin:
        abort(400, "Missing name")
    admin = Admin(**admin)
    admin.save()
    return admin.to_dict(), 201


@app_views.route('/admins/<admin_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_admin(admin_id):
    """updates a admin object
    """
    admin = storage.get(Admin, admin_id)
    if admin is None:
        abort(404)
    update = request.get_json()
    if update is None:
        abort(400, "Not a JSON")
    for key, value in update.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(admin, key, value)
    admin.save()
    return admin.to_dict(), 200
