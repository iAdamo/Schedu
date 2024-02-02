#!/usr/bin/python3
"""Teacher view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.teacher import Teacher


@app_views.route('/teachers', strict_slashes=False)
def teachers():
    """returns a list of all teachers
    """
    return jsonify([teacher.to_dict()
                   for teacher in storage.all(Teacher).values()])


@app_views.route('/teachers/<teacher_id>', strict_slashes=False)
def teacher(teacher_id):
    """returns a teacher object by id
    """
    teacher = storage.get(Teacher, teacher_id)
    if teacher is None:
        abort(404)
    return teacher.to_dict()


@app_views.route('/teachers/<teacher_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_teacher(teacher_id):
    """deletes a teacher object by id
    """
    teacher = storage.get(Teacher, teacher_id)
    if teacher is None:
        abort(404)
    teacher.delete()
    storage.save()
    return {}, 200


@app_views.route('/teachers', methods=['POST'], strict_slashes=False)
def create_teacher():
    """creates a teacher object
    """
    teacher = request.get_json()
    if teacher is None:
        abort(400, "Not a JSON")
    if "name" not in teacher:
        abort(400, "Missing name")
    teacher = Teacher(**teacher)
    teacher.save()
    return teacher.to_dict(), 201


@app_views.route('/teachers/<teacher_id>',
                 methods=['PUT'], strict_slashes=False)
def update_teacher(teacher_id):
    """updates a teacher object
    """
    teacher = storage.get(Teacher, teacher_id)
    if teacher is None:
        abort(404)
    update = request.get_json()
    if update is None:
        abort(400, "Not a JSON")
    for key, value in update.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(teacher, key, value)
    teacher.save()
    return teacher.to_dict(), 200
