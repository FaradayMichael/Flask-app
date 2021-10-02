from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.entities import Users


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember')
    submit = SubmitField('Sign In')


class RegisterForm(LoginForm):
    submit = SubmitField('Register')
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        if Users.query.filter_by(username=username.data).first():
            raise ValidationError("Username already in use.")
