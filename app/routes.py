# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00: CircleStories

import sqlite3

from flask import render_template, redirect, request, url_for, session

from app import app
from app.auth import authenticate_user, create_user


@app.route("/")
@app.route("/index")
def index():
    if "username" in session:
        return render_template("homepage.html", username=session["username"])
    else:
        return render_template("guest.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("index"))

    # GET request: display the form
    if request.method == "GET":
        return render_template("login.html")

    # POST request: handle the form response and redirect
    else:
        username = request.form.get("username", default="")
        password = request.form.get("password", default="")

        if authenticate_user(username, password):
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Username or password incorrect")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        return redirect(url_for("index"))

    # GET request: display the form
    if request.method == "GET":
        return render_template("register.html")

    # POST request: handle the form response and redirect
    else:
        username = request.form.get("username", default="")
        email = request.form.get("email", default="")
        password = request.form.get("password", default="")
        password_check = request.form.get("password_check", default="")

        errors = create_user(username, email, password, password_check)
        if errors:
            return render_template("register.html", errors=errors)
        else:
            # Maybe put a flash message here to confirm everything works
            return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
    return redirect(url_for("index"))


def add_to_db():
    DB_FILE = "discobandit.db"

    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()

    return 1
