from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(UserMixin, db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    pass_hash = db.Column(db.String(), index=True, unique=True)
    adm = db.Column(db.Boolean, index=True, unique=True)
    orders = db.relationship("Orders", backref="user", lazy="dynamic")

    def get_id(self):
        return self.id_user

    def __init__(self, username, adm: bool):
        self.username = username
        self.adm = adm

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Author(db.Model):
    id_author = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(), index=True, unique=True)
    books = db.relationship("Book", backref="author", lazy="dynamic")

    def __init__(self, author_name):
        self.author_name = author_name

    def __repr__(self):
        return self.author_name


class Book(db.Model):
    id_book = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(), index=True, unique=True)
    year = db.Column(db.Integer, index=True, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id_author"))
    orders = db.relationship("Orders", backref="book", lazy="dynamic")

    def __init__(self, book_name, year, author: Author):
        self.book_name = book_name
        self.year = year
        self.author = author

    def __repr__(self):
        return '<Book {}>'.format(self.book_name)


class Orders(db.Model):
    id_order = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, index=True, unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id_book"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_user"))

    def __repr__(self):
        return '<Order {}>'.format(self.id_order)
