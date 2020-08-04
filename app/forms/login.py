from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginBase(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Name', 'autofocus': True})
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={'placeholder': 'Password'})


class LoginForm(LoginBase):
    remember = BooleanField("Remember Me", render_kw={'checked': True})
    submit = SubmitField('Sign In')


class RegisterForm(LoginBase):
    submit = SubmitField('Sign Up')
