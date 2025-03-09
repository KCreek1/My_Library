# database configuration - separate file per duck suggestion
import os

# take out comments for lines 5 & 8 for local development
# from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy 

# load_dotenv(dotenv_path='./.env')
database_url = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)

# print(f"Database URL: {database_url}")

db = SQLAlchemy()

# do not run until ready to start tables. This will create the tables in the database
# but if you do, there is a setting to reset database and thus wiping out all data
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    db.init_app(app)
    with app.app_context():
        db.create_all()
