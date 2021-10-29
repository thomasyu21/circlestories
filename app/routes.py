# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00
# 2021-10-27

from flask import render_template, redirect, url_for

from app import app


@app.route("/")
@app.route("/index")
def index():
    return "Hello, world!"

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return "Registration page"
