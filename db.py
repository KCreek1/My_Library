# database configuration - separate file per duck suggestion
import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy 

load_dotenv(dotenv_path='./.env')
database_url = os.getenv('DATABASE_URL')

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    db.init_app(app)

