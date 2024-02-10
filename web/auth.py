#!/usr/bin/python3
"""auth page for the web application
"""

import os
from flask_login import LoginManager, login_user
from models import storage
from models import teacher
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian
from flask import (
    Flask,
    abort,
    make_response,
    render_template,
    redirect,
    request,
    flash)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_login import login_required, current_user, logout_user
from flask_wtf.csrf import CSRFProtect, CSRFError


app = Flask(__name__)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', '$2b$12$6CMEGRWurPoTczCdfwCf4etJ225UOERcNWhGO/bSPiQSEU8vsuS')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/auth/sign_in'


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
    return redirect('/auth/sign_in')


@app.errorhandler(404)
def page_not_found(e):
    """handle error 404
    """
    return redirect('https://github.com/ibhkh')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.path == '/auth/sign_in':
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    elif request.path == '/auth/sign_out':
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    elif request.path == '/':
        flash('Your session has expired', 'error')
        return redirect('/auth/sign_in')
    else:
        abort(400)


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
        # if user and user.password == password:
        #    return user, user_type
    except Exception as e:
        # Log the exception or print it for debugging
        print(f"Error during user retrieval: {e}")

    return None, None


@app.route('/', strict_slashes=False)
@login_required
def index():
    """Handle the index route
    """
    form = LoginForm()
    user = current_user

    return render_template(f"/{current_user.role}.html", user=user, form=form)


@app.route('/auth/sign_out', methods=['POST'], strict_slashes=False)
@login_required
def sign_out():
    """Handle the sign_out route"""
    if not current_user.is_authenticated:
        return redirect(f"/auth/sign_in")
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(f"/auth/sign_in")


@app.route('/auth/sign_in', methods=['GET', 'POST'], strict_slashes=False)
def sign_in():
    """Handle the sign_in route"""
    if current_user.is_authenticated:
        # Redirect user to their dashboard or another page
        flash('You are already signed in')
        return redirect(f"/")

    form = LoginForm()

    if form.validate_on_submit():
        id = form.id.data
        password = form.password.data

        user, route = authenticate_user(id, password)

        if user:
            login_user(user)
            flash('You have been logged in', 'success')
            response = make_response(redirect(f"/"))
            response.headers['Cache-Control'] = (
                'no-cache, no-store, must-revalidate')
            return response
        else:
            flash('Invalid ID or password', 'error')
            return render_template(
                'login.html', form=form, id=id, password=password)

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
