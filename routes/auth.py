# login, logout, register, password reset

from flask import Blueprint, current_app, render_template, request, flash, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from helpers import apology, get_questions_1, get_questions_2
from models import Users
from database import db

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        # query db for username
        username = request.form.get("username")
        user = Users.query.filter_by(username=username).first()
        
        # make sure username exists and password correct
        if user is None or not check_password_hash(user.hash, request.form.get("password")):
            return apology("Invalid username and/or password", 403)
        
        # remember user
        session["user_id"] = user.id
        
        return redirect("/library")
    
    else:
        return render_template("login.html")
    

@bp.route("/logout")
def logout():
    """Log user out - forget user.id"""
    session.clear()
    flash("You have been logged out", "success")
    return redirect("/")


@bp.route("/passwordreset", methods=["GET", "POST"])
def passwordreset():
    """ reset password """
    if request.method == "POST":
        username = request.form.get("username")
        user = Users.query.filter_by(username=username).first()
        if user:
            session['username'] = username
            security_question_1 = user.security_question_1
            security_question_2 = user.security_question_2
            if "security_answer_1" in request.form and "security_answer_2" in request.form:
                security_answer_1 = request.form.get("security_answer_1")
                security_answer_2 = request.form.get("security_answer_2")
                if not check_password_hash(user.security_answer_1, security_answer_1) or not check_password_hash(user.security_answer_2, security_answer_2):
                    flash("Incorrect answer(s)", "error")
                    return render_template("passwordreset.html", username=username)
                else:
                    return render_template("new_password.html", username=username)
            return render_template("passwordreset.html", username=username, security_question_1=security_question_1, security_question_2=security_question_2)
        else:
            flash("Invalid user name", "error")
            return render_template("passwordreset.html")
    return render_template("passwordreset.html")

@bp.route("/register", methods=["GET", "POST"])
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
            new_user = Users(
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
    
        flash("You have successfully registered and may log in now!", "success")
        return redirect("/login")

    return render_template("register.html", get_questions_1=get_questions_1(), get_questions_2=get_questions_2())

@bp.route("/new_password", methods=["GET", "POST"])
def new_password():
    """ User can change password """
    username = session.get("username")
    
    if not username:
        flash("Session expired or no username", "error")
        return redirect("/passwordreset")
    
    user = Users.query.filter_by(username=username).first()
    if not user:
        flash("Invalid username", "error")
        return redirect("/passwordreset")
    
    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password == "":
            flash("Enter a valid password", "error")
            return redirect("/new_password")
        if password != confirmation:
            flash("Passwords do not match", "error")
            return redirect("/new_password")
        
        hash = generate_password_hash(password, method="pbkdf2:sha1", salt_length=8)
        user.hash = hash
        
        try:
            db.session.commit()
            flash("Password updated", "success")
            
            # Remove the username from the session after the password is successfully updated
            session.pop('username', None)
            
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            flash("Error updating password", "error")
            current_app.logger.error(f"Error updating password: {e}")
            return redirect("/new_password")
    return render_template("new_password.html")

@bp.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    """Delete user account with password confirmation"""
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to delete your account.", "error")
        return redirect("/login")
    
    user = Users.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect("/login")
    
    if request.method == "POST":
        password = request.form.get("password")
        if not check_password_hash(user.hash, password):
            flash("Incorrect password.", "error")
            return render_template("delete_account.html")
        
        try:
            db.session.delete(user)
            db.session.commit()
            session.clear()
            flash("Your account has been deleted.", "success")
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            flash("Error deleting account.", "error")
            current_app.logger.error(f"Error deleting account: {e}")
            return render_template("delete_account.html")
    
    return render_template("delete_account.html")

@bp.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to view your profile.", "error")
        return redirect("/login")
    user = Users.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect("/login")
    return render_template("profile.html", username=user.username)

@bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to change your password.", "error")
        return redirect("/login")
    
    user = Users.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect("/login")
    
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        
        if not check_password_hash(user.hash, current_password):
            flash("Incorrect current password.", "error")
            return render_template("change_password.html")
        if not new_password:
            flash("Enter a new password.", "error")
            return render_template("change_password.html")
        if new_password != confirmation:
            flash("New passwords do not match.", "error")
            return render_template("change_password.html")
        
        user.hash = generate_password_hash(new_password, method="pbkdf2:sha1", salt_length=8)
        try:
            db.session.commit()
            flash("Password changed successfully.", "success")
            return redirect("/profile")
        except Exception as e:
            db.session.rollback()
            flash("Error changing password.", "error")
            current_app.logger.error(f"Error changing password: {e}")
            return render_template("change_password.html")
    
    return render_template("change_password.html", username=user.username)

def register_routes(app):
    app.register_blueprint(bp)
    