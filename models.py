# from gist.github.com/mayukh18/2223bc8fc15263120abd7cbf1efdd41/
# https://gist.github.com/mayukh18/2223bc8fc15263120abd7cbf1efdd41

from database import db
from app import app

# declaring models with db.Model - flask-sqalchemy.readthedocs.io
# https://docs.sqlalchemy.org/en/20/orm/backref.html
# guidance from codieum 
# using db.relationship allows for sqlalchemy to see relationships between tables when querying

class User(db.Model):
    """ table for user personal info"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    displayname = db.Column(db.String(80))
    aboutme = db.Column(db.String(200))
    
class Book(db.Model):
    """ table for books entered into library by any user"""
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_id = db.Column(db.Integer, db.ForeignKey('users.id')) # how to reference other tables
    user = db.relationship('User', backref='books') # per codieum, try backref, plural for many books
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(50), nullable=False)
    is_series = db.Column(db.Boolean, default=False)
    series_name = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(300))
    private = db.Column(db.Boolean, default=False)
    
class Wishlist(db.Model):
    """ table for wishlist for future purchases"""
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    user = db.relationship('User', backref='wishlist')
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    
class Review(db.Model):
    """ table for reviews of books"""    
    __tablename__ = 'review'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    book = db.relationship('Book', backref='reviews')
    username_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='reviews')
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(300), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('book_id', 'username_id', name='unique_review'),
    )
