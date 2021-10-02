from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from app.models import Users
from flask_login import current_user, login_user, logout_user, login_required
from app import db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
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
