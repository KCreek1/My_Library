# reviews

from flask import Blueprint, render_template, request, flash, current_app  # Import current_app for debug check
from helpers import login_required, select_value, get_current_user  # Import get_current_user
from models import Book, Review
from database import db
import os

ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))  # Define ADMIN_USER_ID

bp = Blueprint("reviews", __name__)

@bp.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():
    """ enables users to see reviews for certain books from all users """
    user = get_current_user()  # Define the current user
    select_values = [value for value in select_value() if value not in ('Review', 'Date Read')]  # Exclude non-review fields
    results = None
    pagination = None
    page = request.args.get('page', 1, type=int)
    per_page = 25
        
    if request.method == "GET":
        selection = request.args.get("selection", "").strip() # remove whitespace to avoid empty string
        value = request.args.get("value", "").strip()
        
        attributes = {
            'Title': Book.title,
            'Author': Book.author,
            'Series Name': Book.series_name,
            'Genre': Book.genre,
            'Rating': Review.rating  # Removed Review.review from searchable fields
        }

        if not selection:
            flash("Please enter a search term.", "error")
        elif value not in attributes:
            flash("Invalid search criteria. Please try again.", "error")
        else:
            try:
                # Query reviews for books that match the criteria
                if value == "Rating" and selection.isdigit():
                    query = (
                        db.session.query(Review)
                        .join(Book, Review.book_id == Book.id)
                        .filter(
                            (Review.rating == int(selection)) &
                            ((Book.private == False) | (Book.username_id == user.id))  # Include user's books regardless of private status
                        )
                    )
                elif value != "Rating":
                    query = (
                        db.session.query(Review)
                        .join(Book, Review.book_id == Book.id)
                        .filter(
                            (attributes[value].ilike(f"%{selection.strip()}%")) &
                            ((Book.private == False) | (Book.username_id == user.id))  # Include user's books regardless of private status
                        )
                    )
                else:
                    flash("Invalid rating input. Please enter a valid number.", "error")
                    query = None

                #pagination
                if query is not None:
                    pagination = query.order_by(Book.title.asc()).paginate(page=page, per_page=per_page)
                    results = pagination.items
                    if not results:
                        flash("No reviews found for the selected criteria.", "error")
                else:
                    results = []    

            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                results = []

    return render_template("reviews.html", select_value=select_values, results=results, pagination=pagination)

def register_routes(app):
    app.register_blueprint(bp)
