#!/usr/bin/python3

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', '$2b$12$6CMEGRWurPoTczCdfwCf4etJ225UOERcNWhGO/bSPiQSEU8vsuS')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/auth/sign_in'

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(func):
    """ Decorator to check if user is an admin
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page', 'error')
            return redirect("/")
        return func(*args, **kwargs)
    return decorated_function



from web.schedu import routes
