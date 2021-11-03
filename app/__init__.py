# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00: CircleStories

"""CircleStories

Sets up the app: configures routes, secret key, etc.
"""

from os import urandom

from flask import Flask

app = Flask(__name__)

# This must be after Flask app init to avoid circular imports
from app import routes # pylint: disable=wrong-import-position

# Secret key for session (32 random bytes)
app.secret_key = urandom(32)

# This should be false in prod
app.debug = True
app.run()
