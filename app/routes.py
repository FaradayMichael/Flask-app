from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm, BooksTable, OrdersTable, UsersTable, AddBookForm
from app.models import Users, Book, Orders, Author, Status
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, session
from functools import wraps
from app import db


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.adm:
            redirect(url_for("index"))
        return func(*args, **kwargs)

    return decorated_view


@app.route('/')
@app.route('/index')
@login_required
def index():
    session.clear()
    return render_template('index.html', title="Home")


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))


@app.route("/add_to_cart", methods=['GET', 'POST'])
@login_required
def add_to_cart():
    id_book = request.args.get("id")
    book = Book.query.filter(Book.id_book==int(id_book)).first()
    cart_order = Orders.query.filter(Orders.user==current_user and Orders.status==Status.Active).first()
    if not cart_order:
        cart_order = Orders(user=current_user)
    cart_order.books.append(book)
    db.session.add(cart_order)
    db.session.commit()
    return redirect(request.referrer or url_for("libre"))


@app.route("/add_book", methods=['GET', 'POST'])
@admin_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        author = Author.query.filter(Author.author_name == form.author.data).first()
        if not author:
            author = Author(author_name=form.author.data)
        book = Book(book_name=form.book_name.data, author=author, year=form.year.data, price=form.price.data)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("administration"))
    return render_template("add_book.html", form=form, title="Add Book")


@app.route('/login_', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter(Users.username == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No. Invalid.")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template("login.html", form=form, title="Login")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, adm=False)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Register successfull")
        return redirect(url_for('login'))
    return render_template("register.html", form=form, title="Register")


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    cart_order = Orders.query.filter(Orders.user==current_user and Orders.status==Status.Active).first()
    books = cart_order.books
    print(books)
    cart_table = BooksTable([b.dict for b in books], current_user.adm, False)
    user = Users.query.filter_by(username=username).first_or_404()
    orders = user.orders
    items = [o.dict for o in orders]
    table = OrdersTable(items, user.adm)
    return render_template("user.html", user=user, table=table, cart_table=cart_table, title=username)


@app.route('/libre', methods=['GET', 'POST'])
@login_required
def libre():
    books = Book.query.all()
    books_table = BooksTable(books, current_user.adm, adm_page=False)
    return render_template("libre.html", books=books_table, title="Libre")


@app.route('/administration', methods=['GET', 'POST'])
@login_required
@admin_required
def administration():
    books = Book.query.all()
    books_table = BooksTable(books, current_user.adm, adm_page=True)
    orders = Orders.query.all()
    orders_table = OrdersTable(items=[o.dict for o in orders], adm=current_user.adm)
    users = Users.query.all()
    users_table = UsersTable(users)
    return render_template("administration.html", title="Administration", books=books_table, users=users_table,
                           orders=orders_table)


@app.route("/delete_order", methods=['GET', 'POST'])
@login_required
def delete_order():
    id_order = int(request.args.get('id'))
    order = Orders.query.first_or_404(id_order)
    db.session.delete(order)
    db.session.commit()
    return redirect(request.referrer or url_for("index"))


@app.route("/delete_book", methods=['GET', 'POST'])
@login_required
@admin_required
def delete_book():
    id_book = int(request.args.get("id"))
    book = Book.query.first_or_404(id_book)
    db.session.delete(book)
    db.session.commit()
    return redirect(request.referrer or url_for("index"))
