# routes for add, delete, move books in library and wishlist and reviews

from flask import Blueprint, render_template, request, flash, redirect, current_app
from helpers import login_required, get_current_user, genre_selection, validate_book_id
from models import Book, Wishlist, Review
from database import db

bp = Blueprint("books", __name__)


# Delete book
@bp.route("/delete_book/<string:book_type>", methods=["POST"])
@login_required
def delete_book(book_type):
    """ Enables user to delete books from wishlist or library """
    user = get_current_user()
    book_id = validate_book_id(request.form.get("book_id"))

    if book_id is None:
        flash("Invalid book ID.", "error")
        return redirect("/library" if book_type == "library" else "/wishlist")
    
    try:
        if book_type == "library":
            book = Book.query.filter_by(username_id=user.id).filter_by(id=book_id).first()
            if book:
                # Delete reviews associated with the book
                reviews = Review.query.filter_by(book_id=book.id).all()
                for review in reviews:
                    db.session.delete(review)

                # Delete the book itself
                db.session.delete(book)
                db.session.commit()
                flash("Book and associated reviews deleted", "success")
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
        current_app.logger.error(f"Error deleting book: {e}")

    return redirect("/library" if book_type == "library" else "/wishlist")


@bp.route("/update_book", methods=["GET","POST"])
@login_required    
def update_book():
    """ Allows user to update the details of a book """
    user = get_current_user()
    genres = genre_selection()

    if request.method == "POST":
        book_id = validate_book_id(request.form.get("book_id"))

        if book_id is None:
            flash("Invalid book ID.", "error")
            return redirect("/library")

        book = Book.query.filter_by(username_id=user.id).filter_by(id=book_id).first()
        if book:
            book.title = request.form.get("title")
            book.author = request.form.get("author")
            book.series_name = request.form.get("series_name")
            book.year = request.form.get("year")
            book.genre = request.form.get("genre")
            book.rating = request.form.get("rating")
            book.review = request.form.get("review")
            book.private = request.form.get("private") == "on"

            # Validate year and rating
            if book.year:
                try:
                    book.year = int(book.year)
                except ValueError:
                    flash("Year must be a number.", "error")
                    return render_template("update_book.html", book=book, genres=genres)
                
            if book.rating:
                try:
                    book.rating = int(book.rating)
                except ValueError:
                    flash("Rating must be a number.", "error")
                    return render_template("update_book.html", book=book, genres=genres)
            
            if book.review:
                existing_review = Review.query.filter_by(book_id=book.id, username_id=user.id).first()
                
                if existing_review:
                    # Update the existing review
                    existing_review.rating = book.rating
                    existing_review.review = book.review
                else:
                    # Add new review
                    new_review = Review(
                        book_id=book.id,
                        review=book.review,
                        rating=book.rating,
                        username_id=user.id
                    )
                    db.session.add(new_review)
            
            try:
                db.session.commit()
                flash("Book details updated", "success")
            except Exception as e:
                db.session.rollback()
                flash("Error updating book details", "error")
                current_app.logger.error(f"Error updating book details: {e}")
            
        else:
            flash("Book not found", "error")
        return redirect("/library")
    
    else:
        book_id = validate_book_id(request.args.get("book_id"))

        if book_id is None:
            flash("Invalid book ID.", "error")
            return redirect("/library")
        
        book = Book.query.filter_by(username_id=user.id).filter_by(id=book_id).first()
        return render_template("update_book.html", book=book, genres=genres)
    

@bp.route("/add_book/<string:book_type>", methods=["GET", "POST"])
@login_required
def add_book(book_type):
    """ User adds new book to the library """
    user = get_current_user()
    genres = genre_selection()
    
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        year = request.form.get("year")
        series_name = request.form.get("series_name")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        review = request.form.get("review")
        private = request.form.get("private") == "on"

        # Validate year and rating
        if year:
            try:
                year = int(year)
            except ValueError:
                flash("Year must be a number.", "error")
                return render_template("add_book.html", book_type=book_type)
        if rating:
            try:
                rating = int(rating)
            except ValueError:
                flash("Rating must be a number.", "error")
                return render_template("add_book.html", book_type=book_type)
        else:
            rating = 0  # Default to 0 if no rating provided
        
        # Convert rating to integer if it is provided
        rating = int(rating) if rating else 0  # Default to 0 if no rating provided
        
        if not title or not author or not genre:
            flash("Title, Author, and Genre are required", "error")
            return render_template("add_book.html", book_type=book_type)
        
        # Check if the book already exists
        existing_book = Book.query.filter_by(title=title, author=author).first()
        
        if not existing_book:
            # Create new book if it doesn't exist
            if book_type == "library":
                new_book = Book(username_id=user.id, title=title, author=author, series_name=series_name, year=year, genre=genre, rating=rating, review=review, private=private)
            elif book_type == "wishlist":
                new_book = Wishlist(username_id=user.id, title=title, author=author, series_name=series_name, year=year)
            
            try:
                db.session.add(new_book)
                db.session.commit()
                book_id = new_book.id  # Use the newly created book's ID
            except Exception as e:
                db.session.rollback()
                flash("Error adding book", "error")
                current_app.logger.error(f"Error adding book: {e}")
                return redirect("/library" if book_type == "library" else "/wishlist")
        else:
            # Use existing book if it already exists
            book_id = existing_book.id
        
        # Add a review entry only if the user provided a review and book is in library
        if rating and review and book_type == "library":
            existing_review = Review.query.filter_by(book_id=book_id, username_id=user.id).first()
            
            # Add review only if it doesn't already exist
            if not existing_review:
                new_review = Review(
                    book_id=book_id,  
                    review=review,    
                    rating=rating,    
                    username_id=user.id  
                )

                try:
                    db.session.add(new_review)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    flash("Error adding review", "error")
                    current_app.logger.error(f"Error adding review: {e}")
        
        flash("Book added", "success")
        return redirect("/library" if book_type == "library" else "/wishlist")
    
    else:
        return render_template("add_book.html", book_type=book_type, genres=genres)
    

@bp.route("/move_to_library", methods=["POST"])
@login_required
def move_to_library():
    """ Move book from wishlist to library """
    user = get_current_user()
    book_id = validate_book_id(request.form.get("book_id"))

    if book_id is None:
        flash("Invalid book ID.", "error")
        return redirect("/wishlist")
    
    try:
        wishlist_book = Wishlist.query.filter_by(username_id=user.id).filter_by(id=book_id).first()
        
        if wishlist_book:
            # create new book using wishlist info
            default_genre = 'None'
            
            new_book = Book(
                username_id=user.id,
                title=wishlist_book.title,
                author=wishlist_book.author,
                year=wishlist_book.year,
                genre=default_genre,
                rating=1,
                review=None,
                private=False
            )                                                              
            # add to library
            db.session.add(new_book)
            
            # delete from wishlist
            db.session.delete(wishlist_book)
            
            db.session.commit()
            flash("Book moved to library", "success")
            return redirect("/library")
        else:
            flash("Book not found", "error")
            return redirect("/wishlist")
    except Exception as e:
        db.session.rollback()
        flash("Error moving book", "error")
        current_app.logger.error(f"Error moving book: {e}")
    
    return redirect("/wishlist")

@bp.route("/reviews_to_wishlist", methods=["POST"])
@login_required
def reviews_to_wishlist():
    """Add a book from the reviews section to the current user's wishlist."""
    user = get_current_user()
    book_id = validate_book_id(request.form.get("book_id"))

    if book_id is None:
        flash("Invalid book ID.", "error")
        return redirect("/reviews")

    # Find the book by ID (regardless of owner)
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        flash("Book not found.", "error")
        return redirect("/reviews")

    # Check if already in user's wishlist
    existing = Wishlist.query.filter_by(username_id=user.id, title=book.title, author=book.author).first()
    if existing:
        flash("Book is already in your wishlist.", "info")
        return redirect("/reviews")

    # Add to wishlist (copy book info)
    wishlist_book = Wishlist(
        username_id=user.id,
        title=book.title,
        author=book.author,
        series_name=book.series_name,
        year=book.year
    )
    try:
        db.session.add(wishlist_book)
        db.session.commit()
        flash("Book added to your wishlist!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error adding book to wishlist.", "error")
        current_app.logger.error(f"Error adding book to wishlist: {e}")

    return redirect("/reviews")
    
    
def register_services(app):
    app.register_blueprint(bp)
    