# from gist.github.com/mayukh18/2223bc8fc15263120abd7cbf1efdd41/
# https://gist.github.com/mayukh18/2223bc8fc15263120abd7cbf1efdd41

from manage import db, app

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)
    