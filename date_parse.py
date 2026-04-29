from datetime import datetime
from models import Book, db

# Define a function to parse dates from text
def extract_date_from_review(review):
    # Define possible date formats
    date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%B %d, %Y", "%d %B %Y"]
    
    for fmt in date_formats:
        try:
            # Try to parse the date
            return datetime.strptime(review, fmt).date()
        except ValueError:
            continue
    return None  # Return None if no date is found

# Start a database session
def migrate_dates_from_reviews():
    books = Book.query.all()  # Fetch all books
    for book in books:
        if book.review:  # Check if the review column has data
            date_read = extract_date_from_review(book.review)
            if date_read:
                print(f"Updating book '{book.title}' with date_read: {date_read}")
                book.date_read = date_read  # Move the date to the new column
                book.review = None  # Optionally clear the review column or leave it as is

    # Commit the changes to the database
    db.session.commit()
    print("Migration complete!")

if __name__ == "__main__":
    migrate_dates_from_reviews()