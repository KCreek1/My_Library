import os

from database import db, init_db
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
# all sqlalchemy info from: flask-sqlalchemy.palletsprojects.com
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from routes import auth        # login, logout, passwordreset, register, new_password
from routes import library     # library route
from routes import wishlist    # wishlist route
from routes import reviews     # reviews route
from routes import legal       # privacy, terms
from routes.errors import page_not_found, internal_error
from services import book_services  

__version__ = "1.1.1"

app = Flask(__name__)
bootstrap = Bootstrap(app)

# initiate db
init_db(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """ will display generic info about app """
    return render_template("index.html", version=__version__)

library.register_routes(app)
wishlist.register_routes(app)
reviews.register_routes(app)
auth.register_routes(app)


book_services.register_services(app)


app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_error)
app.register_blueprint(legal.bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
