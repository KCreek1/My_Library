# tests/test_config.py suggested by chat gpt to test w/o heroku
class TestConfig:
    """ Configuration for testing. """
    # Use a separate database for testing
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_database.db"  # Use SQLite for testing, or any other test database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SECRET_KEY = "your_test_secret_key"  # Set a secret key for testing sessions
