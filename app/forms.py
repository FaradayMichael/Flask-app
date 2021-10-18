from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from flask_table import Table, Col, OptCol, ButtonCol, LinkCol
from app.models import Users


class AddBookForm(FlaskForm):
    book_name = StringField("Book Name", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    submit = SubmitField('Add')



class CartTable(Table):
    classes = ['table']
    id_book = Col("Id")
    book_name = Col("Name")
    author = Col("Author")
    year = Col("Year")
    price = Col("Price")
    delete = ButtonCol(name="Delete", endpoint="delete_book", url_kwargs=dict(id="id_book"))

class BooksTable(Table):
    classes = ['table']
    id_book = Col("Id")
    book_name = Col("Name")
    author = Col("Author")
    year = Col("Year")
    price = Col("Price")
    delete = ButtonCol(name="Delete", endpoint="delete_book", url_kwargs=dict(id="id_book"))
    add_to_cart = ButtonCol("Add to Cart", endpoint="add_to_cart", url_kwargs=dict(id="id_book"))

    def __init__(self, items: list, adm, adm_page):
        super().__init__(items)
        self.id_book.show = adm
        self.delete.show = adm_page
        self.add_to_cart.show = not adm_page



class OrdersTable(Table):
    classes = ['table']
    id_order = Col("Id", show=False)
    user = Col("User", show=False)
    books = Col("Book")
    price = Col("Price")
    create_time = Col("Created")
    #is_active = OptCol("Condition", choices={True: "Active", False: "Not active"})
    status = Col("Status")
    delete = ButtonCol(name="Delete", endpoint="delete_order", url_kwargs=dict(id="id_order"))

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
