from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_table import Table, Col

from app.models import Users

class BooksTable(Table):
    classes = ['table']
    id_book = Col("Id")
    book_name = Col("Name")
    year = Col("Year")
    author = Col("Author")


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
