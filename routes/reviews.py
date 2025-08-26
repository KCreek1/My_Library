# reviews

@app.route("/reviews", methods=["GET", "POST"])
@login_required
def reviews():
    """ enables users to see reviews for certain books from all users """
    select_values = select_value()
    results = None
    pagination = None
    page = request.args.get('page', 1, type=int)
    per_page = 25
        
    if request.method == "POST":
        selection = request.form.get("selection","").strip() # remove whitespace to avoid empty string
        value = request.form.get("value", "").strip()
        
        attributes = {
            'Title': Book.title,
            'Author': Book.author,
            'Series Name': Book.series_name,
            'Genre': Book.genre,
            'Rating': Review.rating,
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
                        .join(Book, Review.book_id == Book.id)  # Join the review and book tables        
                        .filter(Review.rating == int(selection), 
                        Book.private == False)
                    )
                    
                elif value != "Rating":
                    query = (
                        db.session.query(Review)
                        .join(Book, Review.book_id == Book.id)
                        .filter(
                        attributes[value].ilike(f"%{selection.strip()}%"),
                        Book.private == False
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