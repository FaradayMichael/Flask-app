from app import db


class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    passw = db.Column(db.String(), index=True, unique=True)
    adm = db.Column(db.Boolean, index=True, unique=True)
    orders = db.relationship("Orders", backref="user", lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Book(db.Model):
    id_book = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(), index=True, unique=True)
    year = db.Column(db.Integer, index=True, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id_author"))
    orders = db.relationship("Orders", backref="book", lazy="dynamic")

    def __repr__(self):
        return '<Book {}>'.format(self.book_name)


class Author(db.Model):
    id_author = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(), index=True, unique=True)
    books = db.relationship("Book", backref="author", lazy="dynamic")

    def __repr__(self):
        return '<Author {}>'.format(self.author_name)


class Orders(db.Model):
    id_order = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, index=True, unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id_book"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_user"))

    def __repr__(self):
        return '<Order {}>'.format(self.id_order)
