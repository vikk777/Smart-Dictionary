from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginBase(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class LoginForm(LoginBase):
    remember = BooleanField("Remember Me")
    submit = SubmitField('Sign In')


class RegisterForm(LoginBase):
    submit = SubmitField('Register')
