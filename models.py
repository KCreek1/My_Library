# from gist.github.com/mayukh18/2223bc8fc15263120abd7cbf1efdd41/
# https://gist.github.com/mayukh18/2223bc8fc15263120abd7cbf1efdd41

from database import db
from app import app

# declaring models with db.Model - flask-sqalchemy.readthedocs.io
# must explicitly name tablename or it will default to class name
# guidance from codieum 
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    displayname = db.Column(db.String(80))
    aboutme = db.Column(db.String(200))
    
class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_id = db.Column(db.Integer, db.ForeignKey('users.id')) # how to reference other tables
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(300))
    
class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username_id = db.Column(db.Integer, db.ForeignKey('users.id')) # how to reference other tables
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
class Reviews(db.Model):    
    __tablename__ = 'reviews'
    book = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    review = db.Column(db.String(300), nullable=False)

