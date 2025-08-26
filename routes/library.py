# main library for user

from flask import Blueprint, render_template, request
from helpers import get_current_user, login_required
from models import Book

bp = Blueprint("library", __name__)

@bp.app.route("/library", methods=["GET", "POST"])
@login_required
def library():
    """Display a table of books in the user's library with advanced search functionality"""
    user = get_current_user()
    books_query = Book.query.filter_by(username_id=user.id)  # Base query for the user's books
    search_term = None

    if request.method == "POST":
        if request.form.get("clear") == "true":
            search_term = ""
        else:
            search_term = request.form.get("search", "").strip()

        if search_term:
            # Dynamically filter by multiple attributes
            try:
                search_rating = int(search_term) 
            except ValueError:
                search_rating = None
            
            books_query = books_query.filter(
                (Book.title.ilike(f"%{search_term}%")) | 
                (Book.author.ilike(f"%{search_term}%")) |
                (Book.series_name.ilike(f"%{search_term}%")) |
                (Book.genre.ilike(f"%{search_term}%")) |
                ((Book.rating == search_rating) if search_rating is not None else False)  # Exact match for integer ratings
            )

    page = request.args.get('page', 1, type=int)
    per_page = 25
    pagination = books_query.order_by(Book.title.asc()).paginate(page=page, per_page=per_page)
    books = pagination.items

    return render_template("library.html", books=books, user=user, search_term=search_term, pagination=pagination)