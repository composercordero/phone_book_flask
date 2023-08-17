from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import PasswordField, EmailField
from wtforms.validators import InputRequired, EqualTo
# from wtforms.validators import EqualTo

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators = [InputRequired()])
    last_name = StringField('Last Name', validators = [InputRequired()])
    phone = StringField('Phone', validators = [InputRequired()])
    address = StringField('Address', validators = [InputRequired()])
    submit = SubmitField('Create contact')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Sign Up')
