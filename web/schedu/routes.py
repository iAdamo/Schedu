#!/usr/bin/python3
"""auth page for the web application
"""


from models import storage
from flask_login import login_user, current_user, logout_user
from flask import abort, make_response, render_template, redirect, request, flash
from flask_login import login_required
from flask_wtf.csrf import CSRFError
from models.student import Student
from web.schedu.forms import LoginForm, StudentRegForm
from web.schedu import *


@login_manager.user_loader
def load_user(user_id):
    """Load user from the database
    """
    try:
        users = {
            'admin': "Admin",
            'teacher': "Teacher",
            'student': "Student",
            'guardian': "Guardian"
        }
        parts = user_id.split('-')
        user_type = parts[1]
        user = users.get(user_type, None)
        if user is None:
            return None

        return storage.get(user, user_id)
    except Exception as e:
        # Log the exception or print it for debugging
        print(f"Error during user retrieval: {e}")
        return None

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/sign_in')

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.path in ('/auth/sign_in', '/auth/sign_out', '/'):
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    else:
        abort(400)

def authenticate_user(id, password):
    """Authenticate user based on user type, ID, and password
    """
    parts = id.split('-')

    try:
        if len(parts) != 4 or parts[0] != 'schedu':
            return None
        user_type = parts[1]
        user = storage.get(user_type.capitalize(), id)

        # Check if user exists and verify password
        if user and bcrypt.check_password_hash(user.password, password):
            return user
    except Exception as e:
        print(f"Error during user retrieval: {e}")

    return None

@app.route('/', strict_slashes=False)
@login_required
def index():
    """Handle the index route
    """
    form = LoginForm()
    user = current_user
    print(f"User: {user}")

    return render_template(f"/{current_user.role}.html", user=user, form=form)

@app.route('/auth/sign_out', methods=['POST'], strict_slashes=False)
@login_required
def sign_out():
    """Handle the sign_out route"""
    if not current_user.is_authenticated:
        return redirect(f"/auth/sign_in")
    logout_user()
    flash('You have been logged out', 'success')
    return redirect("/auth/sign_in")

@app.route('/auth/sign_in', methods=['GET', 'POST'], strict_slashes=False)
def sign_in():
    """Handle the sign_in route"""
    if current_user.is_authenticated:
        # Redirect user to their dashboard or another page
        flash('You are already signed in')
        return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.password.data

        user = authenticate_user(id, password)

        if user:
            login_user(user)
            flash('You have been logged in', 'success')
            response = make_response(redirect("/"))
            response.headers['Cache-Control'] = (
                'no-cache, no-store, must-revalidate')
            return response
        else:
            flash('Invalid ID or password', 'error')
            response = make_response(redirect("/auth/sign_in"))
            response.headers['Cache-Control'] = (
                'no-cache, no-store, must-revalidate')
            return response    

    return render_template('login.html', form=form)


@app.route('/register/student', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def register_student():
    """Handle the student registration route
    """
    form = StudentRegForm()
    if form.validate_on_submit():
        data = form.data
        data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        data.pop('confirm_password')
        data.pop('submit')
        student_count = storage.count("Student") + 1
        data['id'] = f"schedu-student-{data['first_name'][:3]}-{data['last_name'][:3]}-{student_count}".lower()
        student = Student(**data)
        storage.new(student)
        storage.save()
        flash('You have been registered', 'success')
        return redirect("/auth/sign_in")
    return render_template('register_student.html', form=form)
