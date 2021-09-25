from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm, RegisterForm
from app.entities import Users
from app import db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
        # if con.find_user(form.username.data, form.password.data):
        #     pass  # TODO action after login
    return render_template("login.html", form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not Users.query.filter(Users.username==form.username.data).first():
            user = Users(username=form.username.data, passw=form.password.data, adm=False)
            db.session.add(user)
            db.session.commit()
            return redirect('/index')
        else:
            print("no")
            flash("No")
            redirect("/index")
    return render_template("register.html", form=form)
