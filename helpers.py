from flask import redirect, render_template, session
from functools import wraps
from models import Users


def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators
    """        
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Return the current user based on the session."""
    users_id = session["user_id"]
    return Users.query.get(users_id)


def get_questions_1():
    """Return a list of security questions for the user."""
    return [
        'What was your first car?',
        'What is your favorite color?',
        'What is your favorite book?',
        'What was the name of your first pet?',
        'Who is your favorite fictional character?',
        'What is your least favorite book?',
    ]


def get_questions_2():
    """Return a list of additional security questions for the user."""
    return [
        'What is your favorite movie?',
        'What was the name of your first school?',
        'What is your favorite food?', 
        'What is your favorite song?',
        'What is your favorite animal?',
        'What is your favorite band?',
    ]


def select_value():
    """Return a list of values for book entry, searches and filters."""
    return [
        'Title',
        'Author',
        'Series Name',
        'Genre',
        'Rating',
    ]
 
  
def genre_selection():
    """Return a list of genres for book entry."""
    return [
        'Fiction',
        'Non Fiction',
        'Fantasy',
        'Science Fiction',
        'Mystery',  
        'Romance',        
        'Historical',        
        'Biography',        
        'Self Help',        
        'Children',        
        'Young Adult',        
        'Horror',        
        'Poetry',        
        'Classics',        
        'Comics',        
        'Cooking',        
        'Travel',        
        'Art',        
        'Religion',        
        'Philosophy',        
        'Science',        
        'Health',        
        'Business',        
        'Technology',        
        'Music',        
        'Sports',        
        'Parenting',        
        'Adventure',        
        'Spirituality',        
        'Drama',        
        'None',        
    ]

def validate_book_id(book_id):
    """Try to convert book_id to int. Return int if valid, else None."""
    try:
        return int(book_id)
    except (TypeError, ValueError):
        return None
    