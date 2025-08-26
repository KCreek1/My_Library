# routes for add, delete, move books in library and wishlist and reviews

from flask import Blueprint, render_template, request, flash, redirect, current_app
from helpers import login_required, get_current_user, genre_selection
from models import Book, Wishlist, Review
from database import db

bp = Blueprint("books", __name__)


@bp.route("/delete_book/<string:book_type>", methods=["POST"])
@login_required
def delete_book(book_type):
    """ Enables user to delete books from wishlist or library """
    user = get_current_user()
    book_id = request.form.get("book_id")

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
        app.logger.error(f"Error deleting book: {e}")

    return redirect("/library" if book_type == "library" else "/wishlist")


@bp.route("/update_book", methods=["GET","POST"])
@login_required    
def update_book():
    """ Allows user to update the details of a book """
    user = get_current_user()
    genres = genre_selection()

    if request.method == "POST":
        book_id = request.form.get("book_id")
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
                app.logger.error(f"Error updating book details: {e}")
            
        else:
            flash("Book not found", "error")
        return redirect("/library")
    
    else:
        book_id = request.args.get("book_id")
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
                app.logger.error(f"Error adding book: {e}")
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
                    app.logger.error(f"Error adding review: {e}")
        
        flash("Book added", "success")
        return redirect("/library" if book_type == "library" else "/wishlist")
    
    else:
        return render_template("add_book.html", book_type=book_type, genres=genres)
    
    
@bp.route("/delete_book/<string:book_type>", methods=["POST"])
@login_required
def delete_book(book_type):
    """ Enables user to delete books from wishlist or library """
    user = get_current_user()
    book_id = request.form.get("book_id")

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
        app.logger.error(f"Error deleting book: {e}")

    return redirect("/library" if book_type == "library" else "/wishlist")


@bp.route("/update_book", methods=["GET","POST"])
@login_required    
def update_book():
    """ Allows user to update the details of a book """
    user = get_current_user()
    genres = genre_selection()

    if request.method == "POST":
        book_id = request.form.get("book_id")
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
                app.logger.error(f"Error updating book details: {e}")
            
        else:
            flash("Book not found", "error")
        return redirect("/library")
    
    else:
        book_id = request.args.get("book_id")
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
                app.logger.error(f"Error adding book: {e}")
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
                    app.logger.error(f"Error adding review: {e}")
        
        flash("Book added", "success")
        return redirect("/library" if book_type == "library" else "/wishlist")
    
    else:
        return render_template("add_book.html", book_type=book_type, genres=genres)