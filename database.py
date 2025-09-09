import os

# take out comments for lines 4 & 7 for local development
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy 

load_dotenv(dotenv_path='./.env')
database_url = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    db.init_app(app)
    with app.app_context():
        db.create_all()
