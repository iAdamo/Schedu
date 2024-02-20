#!/usr/bin/env python3


from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    PasswordField,
    SubmitField,
    DateField)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError)
from models import storage
from wtforms.validators import Regexp


class BaseRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=3),
        Regexp('^[A-Za-z]*$', message="First name must contain only letters")
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=3),
        Regexp('^[A-Za-z]*$', message="Last name must contain only letters")
    ])
    middle_name = StringField('Middle Name', validators=[
        DataRequired(),
        Length(min=3),
        Regexp('^[A-Za-z]*$', message="Middle name must contain only letters")
    ])
    email = StringField('Email', [Length(min=6, max=35), Email()])
    nin = StringField('NIN', validators=[
        DataRequired(),
        Length(min=11, max=11),
        Regexp('^[0-9]*$', message="NIN must contain only numbers")
    ])
    address = StringField('Address', validators=[DataRequired()])
    date_of_birth = DateField(
        'Date of Birth',
        format='%Y-%m-%d',
        validators=[
            DataRequired()])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=11, max=11),
        Regexp('^[0-9]*$', message="Phone number must contain only numbers")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp(
            r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@%\-_])[A-Za-z\d@%\-_]{8,}$',
            message=("Password must contain at least one uppercase letter, one lowercase letter, one digit, and any special character")
        )
    ])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        record = storage.find(email.data)
        if record == email.data:
            raise ValidationError('Email already exists')

    def validate_nin(self, nin):
        record = storage.find(nin.data)
        if record == nin.data:
            raise ValidationError('NIN already exists')

    def validate_phone_number(self, phone_number):
        record = storage.find(phone_number.data)
        if record == phone_number.data:
            raise ValidationError('Phone number already exists')


class StudentRegForm(BaseRegistrationForm):
    """Form to handle student registration
    """
    pass


class TeacherRegForm(BaseRegistrationForm):
    """Form to handle Teacher's registration
    """
    pass


class GuardianRegForm(BaseRegistrationForm):
    """Form to handle Guardian registration
    """
    pass


class LoginForm(FlaskForm):
    """Form to handle user login
    """
    id = StringField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
