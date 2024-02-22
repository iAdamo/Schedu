#!/usr/bin/env python3
"""routes for the web application
"""

import uuid
from models import storage
from flask_login import login_user, current_user, logout_user
from flask import make_response, render_template, redirect, flash
from flask_login import login_required
from models.guardian import Guardian
from models.student import Student
from models.teacher import Teacher
from web.schedu.forms import (
    GuardianRegForm,
    LoginForm,
    StudentRegForm,
    TeacherRegForm)
from web.schedu import *

# ------------------------------- Login Manager ------------------------------
@login_manager.user_loader
def load_user(user_id):
    """Load user from the database
    """
    return storage.get(None, user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Redirect user to sign in page if not authenticated
    """
    return redirect('/auth/sign_in')

# ---------------------------Login Route -------------------------------------


@app.route('/', strict_slashes=False)
def index():
    """Handle the index route
    """
    return render_template('welcome.html')


@app.route('/dashboard', strict_slashes=False)
@login_required
def dashboard():
    """Handle the dashboard route
    """
    form = LoginForm()
    return render_template(
        f"/dashboard_{current_user.role}.html",
        user=current_user,
        form=form, cache_id=str(uuid.uuid4()))


@app.route('/auth/sign_out', methods=['POST'], strict_slashes=False)
@login_required
def sign_out():
    """Handle the sign_out route
    """
    if not current_user.is_authenticated:
        return redirect("/")
    flash('You have been logged out', 'success')
    logout_user()
    return redirect("/")


@app.route('/auth/sign_in', methods=['GET', 'POST'], strict_slashes=False)
def sign_in():
    """Handle the sign_in route"""
    if current_user.is_authenticated:
        # Redirect user to their dashboard or another page
        flash('You are already signed in')
        response = make_response(redirect("/dashboard"))
        response.headers['Cache-Control'] = (
            'no-cache, no-store, must-revalidate')
        return response

    form = LoginForm()

    if form.validate_on_submit():
        user = storage.get(None, form.id.data)
        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(
                f'Welcome {user.first_name}, You have been logged in',
                'success')
            response = make_response(redirect("/dashboard"))
            response.headers['Cache-Control'] = (
                'no-cache, no-store, must-revalidate')
            return response
        else:
            flash('Invalid ID or password', 'error')
            response = make_response(redirect("/auth/sign_in"))
            response.headers['Cache-Control'] = (
                'no-cache, no-store, must-revalidate')
            return response

    return render_template('login.html', form=form, cache_id=str(uuid.uuid4()))


# ------------------------------- Register Route ----------------------------

def register_user(form, cls, role):
    if form.validate_on_submit():
        data = form.data
        pd = data['password']
        data['password'] = bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        data.pop('confirm_password')
        data.pop('csrf_token')
        data.pop('submit')
        data['name'] = (
            f"{data['first_name']} {data['middle_name']} {data['last_name']}")
        count = storage.count(role) + 1
        data['id'] = f"schedu-{role}-{data['name'][:3]}-{count}".lower()
        data['date_of_birth'] = data['date_of_birth'].strftime('%d-%m-%Y')
        data['role'] = role
        user = cls(**data)
        user.save()
        flash(
            f'{data["name"]} has been registered. id: {data["id"]}, password: {pd}',
            'success')

        response = make_response(redirect("/dashboard"))
        response.headers['Cache-Control'] = (
            'no-cache, no-store, must-revalidate')
        return response
    else:
        print(form.errors)
    return render_template(
        f'reg_{role}.html',
        user=current_user,
        form=form,
        cache_id=str(
            uuid.uuid4()))


@app.route('/register/student', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def register_student():
    """Handle the student registration route"""
    form = StudentRegForm()
    return register_user(form, Student, "student")


@app.route('/register/teacher', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def register_teacher():
    """Handle the teacher registration route"""
    form = TeacherRegForm()  
    return register_user(form, Teacher, "teacher")


@app.route('/register/guardian', methods=['GET', 'POST'], strict_slashes=False)
@admin_required
def register_guardian():
    """Handle the guardian registration route"""
    form = GuardianRegForm()
    return register_user(form, Guardian, "guardian")


@app.route('/profile/<user_id>', strict_slashes=False)
@login_required
def profile(user_id):
    """Handle the profile route"""
    return render_template('profile.html', user_id=user_id, cache_id=str(uuid.uuid4()))
