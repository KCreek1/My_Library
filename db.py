# database configuration - separate file per duck suggestion
import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy 

load_dotenv(dotenv_path='./.env')
db = SQLAlchemy()
database_url = os.getenv('DATABASE_URL')

print(f"Database URL: {database_url}")
