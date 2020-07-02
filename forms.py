from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, AnyOf, Email, email_validator



class RegisterForm(FlaskForm):
    """Form to register a new user"""

    first_name = StringField('First Name', validators = [InputRequired()])
    last_name = StringField('Last Name')
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    email = StringField('Email', validators = [InputRequired()])

class LoginForm(FlaskForm):
    """Form to log in an existing user"""

    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])

class FeedbackForm(FlaskForm):
    """Form to post feedback"""

    title = StringField('Title', validators = [InputRequired()])
    content = StringField('Response', validators = [InputRequired()])

class EditForm(FlaskForm):
    """Form to register a new user"""

    first_name = StringField('First Name', validators = [InputRequired()])
    last_name = StringField('Last Name')
    email = StringField('Email', validators = [InputRequired()])
