#!/usr/bin/python3
"""login.py - login page for the web application
"""

from math import e
import os
from flask_login import LoginManager, login_user
from models import storage
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_login import login_required, current_user, logout_user
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    """Form to handle user login"""
    id = StringField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@login_manager.user_loader 
def load_user(user_id):
    """Load user from the database
    """
    try:
        users = {
            'admin': Admin,
            'teacher': Teacher,
            'student': Student,
            'guardian': Guardian
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
    flash('You must be logged in to access this page.', 'error')
    return redirect('/auth/sign_in')

@app.errorhandler(404)
def page_not_found(e):
    flash('Page not found. Please check the URL and try again.', 'error')
    return redirect('https://github.com/ibhkh')

def authenticate_user(id, password):
    """Authenticate user based on user type, ID, and password
    """
    parts = id.split('-')

    try:
        # Check for valid ID format
        if len(parts) != 4 or parts[0] != 'schedu':
            return None, None  # Return None for both user and user_type

        user_type = parts[1]  # Extract user_type from the ID

        # Check user type and retrieve user object
        user = None
        if user_type == 'admin':
            user = storage.get(Admin, id)
        elif user_type == 'teacher':
            user = storage.get(Teacher, id)
        elif user_type == 'student':
            user = storage.get(Student, id)
        elif user_type == 'guardian':
            user = storage.get(Guardian, id)

        # Check if user exists and verify password
        if user and bcrypt.check_password_hash(user.password, password):
            return user, user_type
    except Exception as e:
        # Log the exception or print it for debugging
        print(f"Error during user retrieval: {e}")

    return None, None


@app.route('/', strict_slashes=False)
def index():
    """Handle the index route"""
    return redirect('/auth/sign_in')


@app.route('/admin', strict_slashes=False)
@login_required
def admin_dashboard():
    """Handle the admin dashboard route
    """
    # Retrieve the current logged-in admin
    admin = storage.get(Admin, current_user.id)
    if admin is None:
        flash('No Admin found for the given id', 'error')
        return redirect('/auth/sign_in')

    # Render the admin dashboard
    return redirect('https://google.com')
    return render_template('admin.html', admin=admin)


@app.route('/teacher', strict_slashes=False)
@login_required
def teacher_dashboard():
    """Handle the teacher dashboard route
    """
    teacher = storage.get(Teacher, current_user.id)
    if teacher is None:
        flash('No Teacher found for the given id', 'error')
        return redirect('/auth/sign_in')
    return render_template('teacher.html', teacher=teacher)


@app.route('/student', strict_slashes=False)
@login_required
def student_dashboard():
    """Handle the student dashboard route
    """
    student = storage.get(Student, current_user.id)
    if student is None:
        flash('No Student found for the given id', 'error')
        return redirect('/auth/sign_in')
    return render_template('student.html', student=student)


@app.route('/guardian', strict_slashes=False)
@login_required
def guardian_dashboard():
    """Handle the guardian dashboard route
    """
    guardian = storage.get(Guardian, current_user.id)
    if guardian is None:
        flash('No Guardian found for the given id', 'error')
        return redirect('/auth/sign_in')
    return render_template('guardian.html', guardian=guardian)


@app.route('/logout', strict_slashes=False)
@login_required
def logout():
    """Handle the logout route
    """
    logout_user()
    flash('You have been logged out', 'info')
    return redirect('/auth/sign_in')


@app.route('/auth/sign_in', methods=['GET', 'POST'], strict_slashes=False)
def sign_in():
    """Handle the sign_in route"""
    form = LoginForm()
    
    if form.validate_on_submit():
        id = form.id.data
        print(id)
        password = form.password.data
        print(password)

        user, route = authenticate_user(id, password)

        if user:
            flash('Login successful!', 'success')
            login_user(user)
            return redirect(f"/{route}")
        else:
            flash('Invalid ID or password', 'error')

    return render_template('login.html', form=form)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
