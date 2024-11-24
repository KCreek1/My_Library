# using framework of finance pset to outline my app
import os

from flask import Flask, flash, redirect, render_template, request, session
# all sqlalchemy info from: flask-sqlalchemy.palletsprojects.com
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import logging
from sqlalchemy.exc import IntegrityError

from database import db, init_db
from helpers import apology, get_current_user, get_questions_1, get_questions_2, login_required, select_value
from models import Book, Review, User, Wishlist

app = Flask(__name__)

# from chatgpt for development purposes and debugging
# Set the environment to development for local development or production for deployment
# os.environ['FLASK_ENV'] = 'development'  # Change to 'production' when deploying

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
    return render_template("index.html")

@app.route("/library")
@login_required
def library():
    """ will display a table of books for the logged in user"""
    user = get_current_user()
    books = Book.query.filter_by(username_id=user.id).all()
    return render_template('library.html', books=books)

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
        if user is None or not check_password_hash(user.hash, request.form.get("password")):
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

@app.route("/passwordreset", methods=["GET", "POST"])
def passwordreset():
    """ reset password """
    if request.method == "POST":
        username = request.form.get("username")
        user = User.query.filter_by(username=username).first()
        if user:
            security_question_1 = user.security_question_1
            security_question_2 = user.security_question_2
            return render_template("passwordreset.html", username=username, security_question_1=security_question_1, security_question_2=security_question_2)
        else:
            return apology("Invalid username")
    
    elif "security_answer_1" in request.form and "security_answer_2" in request.form:
        username = request.form.get("username")
        security_answer_1 = request.form.get("security_answer_1")
        security_answer_2 = request.form.get("security_answer_2")
        user = User.query.filter_by(username=username).first()
    if user:
        if not check_password_hash(user.security_answer_1, security_answer_1) or not check_password_hash(user.security_answer_2, security_answer_2):
            return apology("incorrect answer", 403)
        else:
            return render_template("new_password.html", username=username)
        
    return render_template("passwordreset.html")
        
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
        try:
            db.session.add(new_book)
            db.session.commit()
            flash("Book added to wishlist", "success")
            return redirect("/wishlist")
        except Exception as e:
            db.session.rollback()
            flash("Error adding book to wishlist", "error")
            app.logger.error(f"Error adding book to wishlist: {e}")
            return redirect("/wishlist")        

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
        
        security_question_1 = request.form.get("security_question_1")
        security_question_2 = request.form.get("security_question_2")
        security_answer_1 = request.form.get("security_answer_1")
        security_answer_2 = request.form.get("security_answer_2")
        
        # has security answers
        hashed_security_answer_1 = generate_password_hash(security_answer_1, method="pbkdf2:sha1", salt_length=8)
        hashed_security_answer_2 = generate_password_hash(security_answer_2, method="pbkdf2:sha1", salt_length=8)
       
        # insert into db for login
        try:
            new_user = User(
                username=username, 
                hash=hash, 
                security_question_1=security_question_1, 
                security_question_2=security_question_2, 
                security_answer_1=hashed_security_answer_1, 
                security_answer_2=hashed_security_answer_2
            )
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            return apology("Username already in use")
    
        # success message
        flash("You have successfully registered and may log in now!", "success")
        return redirect("/login")

    return render_template("register.html", get_questions_1=get_questions_1(), get_questions_2=get_questions_2())

@app.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():
    """ enables users to see reviews for certain books """
    select_options = select_value()
        
    if request.method == "POST":
        selection = request.form.get("selection")
        value = request.form.get("value").lower()
        attributes = {
            'Title' : Book.title,
            'Author' : Book.author,
            'Series' : Book.series_name,
            'Genre' : Book.genre,
            'Rating' : Book.rating
        }
        results = Review.query.join(Book).filter(attributes[selection].like('%' + value + '%'), Book.private == False).all()
        if not results:
            return apology("No results found", 403)
        return render_template("reviews.html", select_value=select_value(), results=results)
    return render_template("reviews.html", select_value=select_value(), results=None)    

@app.route("/delete_book/<string:book_type>", methods=["POST"])
@login_required
def delete_book(book_type):
    """ Enables user to delete books from wishlist or library """
    user = get_current_user()
    book_id = request.form.get("book_id")
    try:
        if book_type == "library":
            book = Book.query.filter_by(username_id=user.id).filter_by(id=book_id).first()
            if book:
                db.session.delete(book)
                db.session.commit()
                flash("Book deleted", "success")
                return redirect("/library")
            else:
                flash("Book not found", "error")
        elif book_type == "wishlist":
            wishlist_book = Wishlist.query.filter_by(username_id=user.id).filter_by(id=book_id).first()
            if wishlist_book:
                db.session.delete(wishlist_book)
                db.session.commit()
                flash("Book deleted", "success")
                return redirect("/wishlist")
            else:
                flash("Book not found", "error")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting book", "error")
        app.logger.error(f"Error deleting book: {e}")
    return redirect("/library" if book_type == "library" else "/wishlist")

@app.route("/update_book", methods=["POST"])
@login_required    
def update_book():
    """ Allows user to update the details of a book """
    user = get_current_user()
    book_id = request.form.get("book_id")
    book = Book.query.filter_by(username_id=user.id).filter_by(id=book_id).first()
    if book:
        # simplify with dictionary per codieum
        book_data = {
            "title" : request.form.get("title"),
            "author" : request.form.get("author"),
            "series_name" : request.form.get("series_name"),
            "year" : request.form.get("year"),
            "genre" : request.form.get("genre"),
            "rating" : request.form.get("rating"),
            "review" : request.form.get("review"),
            "private" : request.form.get("private") == "on"
        }
        
        # update book details
        for attr, value in book_data.items():
            if value:
                setattr(book, attr, value)  # Use setattr to set the attribute dynamically based on the key in the dictionary.title:
            
        try:
            db.session.commit()
            flash("Book details updated", "success")
        except Exception as e:
            db.session.rollback()
            flash("Error updating book details", "error")
            app.logger.error(f"Error updating book details: {e}")
            
        return redirect("/library")
    else:
        flash("Book not found", "error")
        return redirect("/library")

@app.route("/add_book/<string:book_type>", methods=["GET", "POST"])
@login_required
def add_book(book_type):
    """ User adds new book to the library """
    user = get_current_user()
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        series_name = request.form.get("series_name")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        review = request.form.get("review")
        private = request.form.get("private") == "on"
        
        if not title or not author or not genre: 
            flash("Title, Author, and Genre are required", "error")
            return render_template("add_book.html")
        
        if book_type == "library":
            new_book = Book(username_id=user.id, title=title, author=author, series_name=series_name, year=year, genre=genre, rating=rating, review=review, private=private)
        elif book_type == "wishlist":
            new_book = Wishlist(username_id=user.id, title=title, author=author, series_name=series_name, year=year)
            
        try:
            db.session.add(new_book)
            db.session.commit()
            flash("Book added", "success")
            return redirect("/library" if book_type == "library" else "/wishlist")
        except Exception as e:
            db.session.rollback()
            flash("Error adding book", "error")
            app.logger.error(f"Error adding book: {e}")
            return redirect("/library" if book_type == "library" else "/wishlist")
    else:
        return render_template("add_book.html")

@app.route("/new_password", methods=["GET", "POST"])
@login_required
def new_password():
    """ User can change password """
    if request.method == "POST":
        user = get_current_user()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password == "":
            return apology("Enter a valid password")
        if password != confirmation:
            return apology("Passwords do not match")
        hash = generate_password_hash(password, method="pbkdf2:sha1", salt_length=8)
        user.hash = hash
        
        try:
            db.session.commit()
            flash("Password updated", "success")
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            flash("Error updating password", "error")
            app.logger.error(f"Error updating password: {e}")
            return redirect("/new_password")
    return render_template("new_password.html")

# copied from chat gpt to log errors
# 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f"404 Error: {e}, Route: {request.url}")  # Log with route
    return apology("Page not found", 404)

# 500 Error Handler
@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f"500 Error: {e}, Route: {request.url}")  # Log with route
    return apology("Internal server error", 500)

# Running the app
# if __name__ == '__main__':
    # app.run(debug=debug_mode)  # Will automatically set debug=True in development mode
    