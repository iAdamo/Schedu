#!/usr/bin/python3
"""Student view objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.student import Student


@app_views.route('/students', strict_slashes=False)
def students():
    """returns a list of all students
    """
    return jsonify([student.to_dict()
                   for student in storage.all(Student).values()])


@app_views.route('/students/<student_id>', strict_slashes=False)
def student(student_id):
    """returns a student object by id
    """
    student = storage.get(Student, student_id)
    if student is None:
        abort(404)
    return student.to_dict()


@app_views.route('/students/<student_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_student(student_id):
    """deletes a student object by id
    """
    student = storage.get(Student, student_id)
    if student is None:
        abort(404)
    student.delete()
    storage.save()
    return {}, 200


@app_views.route('/students', methods=['POST'], strict_slashes=False)
def create_student():
    """creates a student object
    """
    student = request.get_json()
    if student is None:
        abort(400, "Not a JSON")
    if "first_name" not in student:
        abort(400, "Missing name")
    if "nin" not in student:
        abort(400, "Missing nin")
    """if "email" not in student:
        abort(400, "Missing email")
    if "phone_number" not in student:
        abort(400, "Missing phone_number")"""

    # Check if a student with the same nin, email, or phone number already
    # exists
    existing_students = storage.all(Student).values()

    # Check if nin is exactly 11 digits
    if len(student["nin"]) != 11:
        abort(400, "The nin must be exactly 11 digits")

    # Check for duplicate nin
    if any(s.nin == student["nin"] for s in existing_students):
        abort(400, "A student with this nin already exists")

    # Check for duplicate email
    if any(s.email == student["email"] for s in existing_students):
        abort(400, "A student with this email already exists")

    # Check for duplicate phone number
    if any(s.phone_number == student["phone_number"]
           for s in existing_students):
        abort(400, "A student with this phone number already exists")

    student = Student(**student)
    student.save()
    return student.to_dict(), 201


@app_views.route('/students/<student_id>',
                 methods=['PUT'], strict_slashes=False)
def update_student(student_id):
    """updates a student object
    """
    student = storage.get(Student, student_id)
    if student is None:
        abort(404)
    update = request.get_json()
    if update is None:
        abort(400, "Not a JSON")
    for key, value in update.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(student, key, value)
    student.save()
    return student.to_dict(), 200
