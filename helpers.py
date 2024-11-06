import requests

from flask import redirect, render_template, session
from functools import wraps

from models import User

# using apology helper from finance pset
def apology(message, code=400):
    
    def escape(s):
        """
        Escape special characters
        https://gihub.com/jacebrowning/memgen#special-characters
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
    user_id = session["user_id"]
    return User.query.get(user_id)
