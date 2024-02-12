from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo


class StudentRegForm(FlaskForm):
    """Form to handle student registration
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nin = IntegerField('NIN', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    submit = SubmitField('Register')


class TeacherRegForm(FlaskForm):
    """Form to handle Teacher's registration
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
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
    email = StringField('Email', validators=[DataRequired(), Email()])
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
