from flask import redirect, render_template, session
from functools import wraps

from models import Users

# using apology helper from finance pset
def apology(message, code=400):
    
    def escape(s):
        """
        Escape special characters
        https://github.com/jacebrowning/memgen#special-characters
        """
            
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s
    
    return render_template("apology.html", top=code, bottom=escape(message)), code

# using login_required from finance helpers
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
    users_id = session["user_id"]
    return Users.query.get(users_id)

def get_questions_1():
    return [
        'What was your first car?',
        'What is your favorite color?',
        'What is your favorite book?',
        'What was the name of your first pet?',
        'Who is your favorite fictional character?',
        'What is your least favorite book?',
    ]
    
def get_questions_2():
    return [
        'What is your favorite movie?',
        'What was the name of your first school?',
        'What is your favorite food?', 
        'What is your favorite song?',
        'What is your favorite animal?',
        'What is your favorite band?',
    ]
    
def select_value():
    return [
        'Title',
        'Author',
        'Series Name',
        'Genre',
        'Rating',
    ]
 
 # genre list for book entry   
def genre_selection():
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
