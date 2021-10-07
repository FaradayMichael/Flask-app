from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_table import Table, Col, OptCol

from app.models import Users


class BooksTable(Table):
    classes = ['table']
    id_book = Col("Id")
    book_name = Col("Name")
    year = Col("Year")
    author = Col("Author")

    def __init__(self, items: list, adm):
        super().__init__(items)
        self.id_book.show = adm


class OrdersTable(Table):
    classes = ['table']
    id_order = Col("Id", show=False)
    user = Col("User", show=False)
    book_name = Col("Book")
    book_author = Col("Author")
    price = Col("Price")
    create_time = Col("Created")
    is_active = OptCol("Condition", choices={True: "Active", False: "Not active"})

    def __init__(self, items: list, adm):
        super().__init__(items)
        self.id_order.show = adm
        self.user.show = adm


class UsersTable(Table):
    classes = ['table']
    id_user = Col("Id")
    username = Col("Username")
    pass_hash = Col("Password hash")
    adm = OptCol("Role", choices={True: "Admin", False: "User"})

    def __init__(self, items: list):
        super().__init__(items)
        self.pass_hash.show = False


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
