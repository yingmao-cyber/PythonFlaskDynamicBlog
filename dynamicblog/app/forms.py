from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    # Use class method to represent forms through Flask-WTF library
    username = StringField('Username', validators=[DataRequired(message="Username is required!")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required!")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # this validator will be added to according validators array automatically
        # function name must be in the format of validator_<field_name>
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            # raise is from JavaScript
            # this will be displayed as error in front-end through error in form.<>.errors defined in html
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')


class DeleteForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required!")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required!")])
    submit = SubmitField('Confirm to Delete')
