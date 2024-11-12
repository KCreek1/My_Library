# using framework of finance pset to outline my app
import os

from flask import Flask, flash, redirect, render_template, request, session
# all sqlalchemy info from: flask-sqlalchemy.palletsprojects.com
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from database import db, init_db
from helpers import apology, get_current_user,login_required
from models import Book, User, Wishlist, Review

app = Flask(__name__)
# setting up db for sqlalchemy
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
def index():
    """ will display generic info about app """
    
    # what do I want the page to display
    return render_template("index.html")
   
@app.route("/mybooks")
@login_required
def mybooks():
    """ will display a table of books for the logged in user"""
    
   # TODO: ADD SEARCH BUTTON TO THIS PAGE
    books = Book.query.filter_by(private=False).all()
    
    return render_template('mybooks.html', books=books)
    
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
        
        return redirect("/library")
    
    # if by GET
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    
    # forget user
    session.clear()
    
    return redirect("/")

@app.route("/passwordreset")
@login_required
def passwordreset():
    """ reset password """
    #TODO
    return apology("to do")


@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    """ will return a list of books that the user has added to their wishlist"""      
    if request.method == "GET":
        user = get_current_user()
        username = user.username
        wishlist = Wishlist.query.filter_by(username_id=username).all()
        return render_template('wishlist.html', wishlist=wishlist)

    elif request.method == "POST":
        if not request.form["title"]:
            return apology("must provide title", 403)
        elif not request.form["author"]:
            return apology("must provide author", 403)
        title = request.form["title"]
        author = request.form["author"]
        series_name = request.form["series_name"]
        year = request.form["year"]
        new_book = Wishlist(title=title, author=author, series_name=series_name, year=year)
        db.session.add(new_book)
        db.session.commit()
        return redirect("/wishlist")
        
# need to add a db interaction for adding to/deleting from wishlist

@app.route("/register", methods=["GET", "POST"])
def register():
    """ register a new user """
    
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
    
        # success message
        flash("You have succesfully registered and may log in now!", "success")
        # send to login
        return redirect("/login")

    return render_template("register.html")

@app.route("/library")
@login_required
def library():
    """ will return a list of books for the particular user who is signed in """
    
    user = get_current_user()
    books = Book.query.filter_by(username_id=user.id).all()
    return render_template('library.html', books=books)    
    

@app.route("/search")
@login_required
def search():
    # TODO
    return apology("to do")

@app.route("/delete_book", methods=["POST"])
@login_required
def delete_book():
    """ Enables user to delete books from wishlist or library """
    book_id = request.form["book_id"]  # assigns book_id from unique id in table
    book = Book.query.filter_by(username_id=get_current_user().id).filter_by(id=book_id).first()
    if book:
        db.session.delete(book)
        db.session.commit
        flash("Book deleted", "success")
        return redirect("/library")
    else:
        wishlist_book = Wishlist.query.filter_by(username_id=get_current_user().id).filter_by(id=book_id).first()
        if wishlist_book:
            db.session.delete(wishlist_book)
            db.session.commit()
            flash("Book deleted", "success")
            return redirect("/wishlist")
        else:
            flash("Book not found", "error")
            
@app.route("/update_book", methods=["POST"])
@login_required    
def update_book():
    """ Allows user to update the details of a book """
    book_id = request.form["book_id"]  # assigns book_id from unique id in table
    book = Book.query.filter_by(username_id=get_current_user().id).filter_by(id=book_id).first()
    if book:
        if request.method == "POST":
        # update book if form is submitted
            #codieum assistance with method to be used
            title = request.form.get("title")
            author = request.form.get("author")
            series_name = request.form.get("series_name")
            year = request.form.get("year")
            genre = request.form.get("genre")
            rating = request.form.get("rating")
            review = request.form.get("review")
            private = request.form.get("private") == "on"
        
        
            if title:
                book.title = title
            if author:
                book.author = author
            if year:
                book.year = year
            if series_name:
                book.series_name = series_name
            if genre:
                book.genre = genre
            if rating:
                book.rating = rating
            if review:
                book.review = review
            if private:
                book.private = private
    
            db.session.commit()
            flash("Book details updated", "success")
            return redirect("/library")
        else:
            # will just resubmit the same data
            return render_template("update_book.html", book=book)
    else:
        flash("Book not found", "error")
        return redirect("/library")
    
@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    """ User adds new book to the library """
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        series_name = request.form.get("series_name")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        review = request.form.get("review")
        private = request.form.get("private") == "on" # if box is checked, private is true
        if not title or not author or not genre: 
            flash("Title, Author, and Genre are required", "error")
            return render_template("add_book.html")
        new_book = Book(title=title, author=author, series_name=series_name, year=year, genre=genre, rating=rating, review=review)
        db.session.add(new_book)
        db.session.commit()
        return redirect("/library")
    else:
        return render_template("add_book.html")