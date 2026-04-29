# main library for user

import os

from flask import Blueprint, render_template, request, current_app, flash
from helpers import get_current_user, login_required, select_value  # Import select_value
from models import Book

bp = Blueprint("library", __name__)

ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))

@bp.route("/library", methods=["GET", "POST"])
@login_required
def library():
    """Display a table of books in the user's library with advanced search functionality"""
    user = get_current_user()

    if user.id == ADMIN_USER_ID and current_app.debug:
        books_query = Book.query
    else:
        books_query = Book.query.filter_by(username_id=user.id)  #  Base query for the user's books
    search_term = None

    if request.method == "GET":
        selection = request.args.get("selection", "").strip()
        value = request.args.get("value", "").strip()

        attributes = {
            'Title': Book.title,
            'Author': Book.author,
            'Series Name': Book.series_name,
            'Genre': Book.genre,
            'Rating': Book.rating,
            'Review': Book.review
        }

        if not selection:
            flash("Please enter a search term.", "error")
        elif value not in attributes:
            flash("Invalid search criteria. Please try again.", "error")
        else:
            try:
                if value == "Rating" and selection.isdigit():
                    books_query = books_query.filter(
                        Book.rating == int(selection)
                    )
                elif value != "Rating":
                    books_query = books_query.filter(
                        attributes[value].ilike(f"%{selection}%")
                    )
                else:
                    flash("Invalid rating input. Please enter a valid number.", "error")

            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")

    page = request.args.get('page', 1, type=int)
    per_page = 25
    pagination = books_query.order_by(Book.title.asc()).paginate(page=page, per_page=per_page)
    books = pagination.items

    select_values = select_value()  # Get dropdown options

    return render_template("library.html", books=books, user=user, search_term=search_term, pagination=pagination, select_value=select_values)

def register_routes(app):
    app.register_blueprint(bp)
