from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import storage

class StudentRegForm(FlaskForm):
    """Form to handle student registration
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', [Length(min=6, max=35), Email()])
    nin = IntegerField('NIN', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of Birth', format='%d-%m-%Y')
    submit = SubmitField('Register')
    

    def validate_email(self, email):
        """Check if email already exists
        """
        student = storage.get("Student", None)
        for stud in student:
            if stud.email == email.data:
                raise ValidationError('Email already exists')
            
    def validate_nin(self, nin):
        """Check if NIN already exists
        """
        student = storage.get("Student", None)
        for stud in student:
            if stud.nin == nin.data:
                raise ValidationError('NIN already exists')
            
    def validate_phone_number(self, phone_number):
        """Check if phone number already exists
        """
        student = storage.get("Student", None)
        for stud in student:
            if stud.phone_number == phone_number.data:
                raise ValidationError('Phone number already exists')


class TeacherRegForm(FlaskForm):
    """Form to handle Teacher's registration
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', [Length(min=6, max=35), Email()])
    nin = IntegerField('NIN', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    subject = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Register')


class GuardianRegForm(FlaskForm):
    """Form to handle Guardian registration
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', [Length(min=6, max=35), Email()])
    nin = IntegerField('NIN', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    student_id = StringField('Student ID', validators=[DataRequired()])
    relationship_to_student = SelectField(
        'Relationship to Student', choices=[
            ('parent', 'Parent'), ('guardian', 'Guardian')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Form to handle user login
    """
    id = StringField('ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
