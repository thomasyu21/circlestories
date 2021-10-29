# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00
# 2021-10-27

from os import urandom

from flask import Flask

app = Flask(__name__)

# Secret key for session (32 random bytes)
app.secret_key = urandom(32)

from app import routes

app.debug = True
app.run()
