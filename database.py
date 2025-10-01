import os

# Always load .env if running locally (safe for local, ignored on Heroku)
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path='./.env')
except ImportError:
    pass

from flask_sqlalchemy import SQLAlchemy

database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise RuntimeError("DATABASE_URL is not set in environment variables or .env file.")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    db.init_app(app)
    with app.app_context():
        db.create_all()
