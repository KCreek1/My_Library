# database configuration - separate file per duck suggestion
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(dotenv_path='./.env')

database_url = os.getenv('DATABASE_URL')

# geeks for geeks postgresql connection
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT', 5432)
database = os.getenv('DB_NAME')

def get_connection():
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database
        )   
    )

if __name__ == '__main__':
    try:
        # get connection
        engine = get_connection()
        print("connection to  datbase successsful")
    except Exception as ex:
        print("connection to database failed \n", ex)
    
