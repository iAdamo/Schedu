#!/usr/bin/python3
"""login.py - login page for the web application
"""

from flask_login import login_user
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


app = Flask(__name__)
bcrypt = Bcrypt(app)


class LoginForm(FlaskForm):
    """Form to handle user login"""
    id = StringField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


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
    return redirect(url_for('auth/sign_in'))


@app.route('/dashboard/admin', strict_slashes=False)
@login_required
def admin_dashboard():
    """Handle the admin dashboard route
    """
    # Retrieve the current logged-in admin
    admin = storage.get(Admin, current_user.id)
    if admin is None:
        flash('No Admin found for the given id', 'error')
        return redirect(url_for('auth/sign_in'))

    # Render the admin dashboard
    return render_template('admin.html', admin=admin)


@app.route('/dashboard/teacher', strict_slashes=False)
@login_required
def teacher_dashboard():
    """Handle the teacher dashboard route
    """
    teacher = storage.get(Teacher, current_user.id)
    if teacher is None:
        flash('No Teacher found for the given id', 'error')
        return redirect(url_for('auth/sign_in'))
    return render_template('teacher.html', teacher=teacher)


@app.route('/dashboard/student', strict_slashes=False)
@login_required
def student_dashboard():
    """Handle the student dashboard route
    """
    student = storage.get(Student, current_user.id)
    if student is None:
        flash('No Student found for the given id', 'error')
        return redirect(url_for('auth/sign_in'))
    return render_template('student.html', student=student)


@app.route('/dashboard/guardian', strict_slashes=False)
@login_required
def guardian_dashboard():
    """Handle the guardian dashboard route
    """
    guardian = storage.get(Guardian, current_user.id)
    if guardian is None:
        flash('No Guardian found for the given id', 'error')
        return redirect(url_for('auth/sign_in'))
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
def login():
    """Handle the login route"""
    form = LoginForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.password.data

        user, user_type = authenticate_user(id, password)

        if user:
            flash('Login successful!', 'success')
            login_user(user)
            return redirect(url_for(f'/dashboard/{user_type}'))
        else:
            flash('Invalid ID or password', 'error')

    return render_template('sign_in.html', form=form)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
