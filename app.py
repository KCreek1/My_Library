# using framework of finance pset to outline my app
import os

from flask import Flask, flash, redirect, render_template, request, session
# all sqlalchemy info from: flask-sqlalchemy.palletsprojects.com
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from db import db, init_db
from helpers import apology, login_required

app = Flask(__name__)
# setting up postgresql db in db.py
init_db(app)

# from finance - Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# from finance
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Content-Type"] = "text/html; charset=utf-8"  # Ensure correct content-type
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    # retrieve user_id
    user_id = session.get("user_id")
    if not session.get("user_id"):
        return redirect("login")
    
    # what do I want the page to display
    
    return render_template("index.html")

# using login route from finance pset

@app.route("/login", methods=["GET", "POST"])
def login():
    
    # Forget any user_id
    session.clear()
    
    # If via POST (using form)
    if request.method == "POST":
        # make sure user name submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        # make sure password submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        # query db for username
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        
        # make sure username exists and password correct
        # improved for sqlalchemy per copilot
        if user is None or not check_password_hash(
            user.hash, request.form.get("password")):
            return apology("invalid username and/or password", 403)
        
        # remember user
        session["user_id"] = user.id
        
        return redirect("/")
    
    # if by GET
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    
    # forget user
    session.clear()
    
    return redirect("/")

@app.route("/passwordreset")
def passwordreset():
    #TODO
    return apology("to do")

@app.route("/peruse")
def peruse():
    #TODO
    return apology("to do")

@app.route("/wishlist")
def wishlist():
    #TODO
    return apology("to do")

@app.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        # set username
        username = request.form.get("username")
        if not username:
            return apology("Enter a valid username")
        
        # confirm password entered and matches confirmation
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password == "":
            return apology("Enter a valid password")
        if password != confirmation:
            return apology("Passwords do not match")
    
        # create hash with salt to ensure unique value
        hash = generate_password_hash(password, method="pbkdf2:sha1", salt_length=8)
    
        # insert into db for login
        try:
            # need to set up sqlalchemy db
            # ddb advice how to convert db.execute to sqlalchemy
           new_user = User(username=username, hash=hash)
           db.session.add(new_user)
           db.session.commit()
        # MUST set username as a UNIQUE identifier
        except Exception:
            return apology("Username already in use")
    
        # send to login
        return redirect("/login")

    return render_template("register.html")