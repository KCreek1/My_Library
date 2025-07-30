from sqlalchemy import CheckConstraint
from database import db


class Users(db.Model):
    """ table for user personal info"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    security_question_1 = db.Column(db.String(100), nullable=False)
    security_question_2 = db.Column(db.String(100), nullable=False)
    security_answer_1 = db.Column(db.String(100), nullable=False)
    security_answer_2 = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), default=None) # not currently in use - but may be in the future
    about_me = db.Column(db.String(300), default=None) # not currently in use - but may be in the future

    
class Book(db.Model):
    """ table for books entered into library by any user"""
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref='books') # backref, plural for many books
    title = db.Column(db.String(150), nullable=False, default='Untitled')
    author = db.Column(db.String(50), nullable=False, default='Unknown')
    year = db.Column(db.String(4), default='Unknown')
    genre = db.Column(db.String(50), nullable=False, default='None') # will use list to limit choices
    series_name = db.Column(db.String(50), default='None')
    rating = db.Column(db.Integer, default=0)
    review = db.Column(db.String(300), default='No review yet') 
    private = db.Column(db.Boolean, default=False)
    

class Wishlist(db.Model):
    """ table for wishlist for future purchases"""
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    user = db.relationship('Users', backref='wishlist')
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    series_name = db.Column(db.String(50), nullable=True)
    year = db.Column(db.String(4), default='None')
    

class Review(db.Model):
    """ table for reviews of books"""    
    __tablename__ = 'review'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    book = db.relationship('Book', backref='reviews', primaryjoin="and_(Review.book_id==Book.id, Book.private==False)")
    username_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='reviews')
    rating = db.Column(db.Integer, default=0)
    review = db.Column(db.String(300), default='No review yet', nullable=False)

    __table_args__ = (
        db.UniqueConstraint('book_id', 'username_id', name='unique_review'),
        CheckConstraint('rating >= 0 and rating <= 5', name='rating_range')
    )
