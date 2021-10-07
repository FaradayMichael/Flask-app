from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm, BooksTable, OrdersTable, UsersTable
from app.models import Users, Book, Orders
from flask_login import current_user, login_user, logout_user, login_required

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
    return render_template('index.html', title="Home")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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


@app.route('/user/<username>')
@login_required
def user(username):
    user = Users.query.filter_by(username=username).first_or_404()
    orders = user.orders
    items = [o.dict for o in orders]
    table = OrdersTable(items, user.adm)
    return render_template("user.html", user=user, table=table, title=username)


@app.route('/libre', methods=['GET', 'POST'])
@login_required
def libre():
    books = Book.query.all()
    books_table = BooksTable(books, current_user.adm)
    return render_template("libre.html", books=books_table, title="Libre")


@app.route('/administration', methods=['GET', 'POST'])
@login_required
@admin_required
def administration():
    books = Book.query.all()
    books_table = BooksTable(books, current_user.adm)
    orders = Orders.query.all()
    orders_table = OrdersTable(items=[o.dict for o in orders], adm=current_user.adm)
    users = Users.query.all()
    users_table = UsersTable(users)
    return render_template("administration.html", title="Administration", books=books_table, users=users_table,
                           orders=orders_table)
