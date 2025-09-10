from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

# imports for login mechanism
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint("auth", __name__)

@auth.route("/debug")
def debug():
    from main import app
    return app.config['SQLALCHEMY_DATABASE_URI']

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(Email=email).first()

        print(user)

        if user:
            if check_password_hash(user.Password, password):
                flash("Logged in successfully.", category="success")
                
                # login mechanism, log in user
                login_user(user, remember=True)

            else:
                flash("Incorrect password.", category="error")
        else:
            flash("User not exists.", category="error")

    # login mechanism
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():

    # logout mechanism
    logout_user()

    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=["POST", "GET"])
def signup():
    
    if request.method == "POST":

        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password = request.form.get("password")
        passwordConfirm = request.form.get("passwordConfirm")

        user = User.query.filter_by(Email=email).first()

        if user:
            flash("User already exists.", category="error")
        # data check logic goes here
        elif len(email) > 0:
            if password != passwordConfirm:
                flash("Password must match.", category="error")
            else:
                new_user = User(Email=email, FirstName=firstName, Password=generate_password_hash(password, method="pbkdf2:sha256"))
                db.session.add(new_user)
                db.session.commit()
                
                # login mechanism, log in user as they sign up
                login_user(user, remember=True)
                
                flash("Account created!", category="success")
                # one could just use /, but using blueprint name / fuction name in case if you change the url for home function, don't have to change this url again
                return redirect(url_for("views.home"))
        else:
            flash("Account information needed.", category="error")

    # login mechanism
    return render_template("signup.html", user=current_user)