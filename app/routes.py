# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00
# 2021-10-27

from flask import render_template, redirect, url_for, session
import sqlite3
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
    return render_template("register.html")

def add_to_db():
    DB_FILE="discobandit.db"

    db = sqlite3.connect(DB_FILE) # open if file exists, otherwise create
    c = db.cursor() 

    return 1

