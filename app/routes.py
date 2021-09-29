from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegisterForm
from app.entities import Users
from flask_login import current_user, login_user, logout_user
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter(Users.username == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not Users.query.filter(Users.username == form.username.data).first():
            user = Users(username=form.username.data, passw=form.password.data, adm=False)
            db.session.add(user)
            db.session.commit()
            return redirect('/index')
        else:
            flash("No")
            redirect("/index")
    return render_template("register.html", form=form)
