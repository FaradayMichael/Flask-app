from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy_serializer import SerializerMixin
from enum import Enum


@login.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model, SerializerMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    pass_hash = db.Column(db.String())
    adm = db.Column(db.Boolean)
    orders = db.relationship("Orders", backref="user", lazy='subquery')

    def get_id(self):
        return self.id_user

    def __init__(self, username, adm: bool):
        self.username = username
        self.adm = adm

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __eq__(self, other):
        return self.username == other.username

    def __repr__(self):
        return self.username


class Author(db.Model, SerializerMixin):
    __tablename__ = 'author'
    serialize_rules = ('-books.author',)

    id_author = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(), index=True)
    books = db.relationship("Book", backref="author", lazy='subquery')

    def __init__(self, author_name):
        self.author_name = author_name

    def __repr__(self):
        return self.author_name

    def __eq__(self, other):
        return self.author_name == other.author_name


orders_book = db.Table(
    'orders_book',
    db.Column("order_id", db.Integer(), db.ForeignKey("orders.id_order")),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id_book"))
)


class Book(db.Model, SerializerMixin):
    __tablename__ = "book"

    id_book = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id_author"))
    year = db.Column(db.Integer)
    price = db.Column(db.Integer)

    # orders = db.relationship("Orders", secondary="link", primaryjoin="Book.id_book==Link.book_id")

    def __init__(self, book_name, author: Author, year, price):
        self.book_name = book_name
        self.year = year
        self.author = author
        self.price = price

    @property
    def dict(self):
        return dict(id_book=self.id_book, book_name=self.book_name, author=self.author, year=self.year,
                    price=self.price)

    def __repr__(self):
        return self.book_name


class Status(Enum):
    Active = "Active"
    Opened = "Opened"
    Closed = "Closed"


class Orders(db.Model):
    __tablename__ = "orders"
    id_order = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    books = db.relationship("Book", secondary="orders_book", backref=db.backref('orders', lazy='subquery'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_user"))
    create_time = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    status = db.Column(db.Enum(Status), default=Status.Active)

    @property
    def dict(self):
        return dict(id_order=self.id_order, user=self.user, books=self.books,
                    create_time=self.create_time,
                    price=self.price, status=self.status)

    def __repr__(self):
        return '<Order {}>'.format(self.id_order)
