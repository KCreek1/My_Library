import pytest
from app import app
from config import TestConfig
from flask_sqlalchemy import SQLAlchemy
from models import User

db = SQLAlchemy(app)

# Fixture to set up the test app
@pytest.fixture(scope="module")
def test_app():
    app.config.from_object(TestConfig)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

# Fixture to create a test client
@pytest.fixture(scope="module")
def test_client(test_app):
    return test_app.test_client()

# Fixture to create a test user
@pytest.fixture(scope="module")
def test_user(test_app):
    with test_app.app_context():
        new_user = User(username="testuser", hash="testpasswordhash")
        db.session.add(new_user)
        db.session.commit()
        return new_user

# Test for index route
def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

# Test for login route
def test_login(test_client, test_user):
    response = test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302
    assert response.location == "/library"
    with test_client.session_transaction() as session:
        assert session['_user_id'] == test_user.id  # Check if user ID is set in the session

# Test for library route
def test_library(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.get('/library')
    assert response.status_code == 200
    assert b"Library" in response.data

# Test for logout route
def test_logout(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.get('/logout')
    assert response.status_code == 302
    assert response.location == "/"

# Test for password reset route
def test_passwordreset(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.get('/passwordreset')
    assert response.status_code == 200
    assert b"Password Reset" in response.data

# Test for wishlist route
def test_wishlist(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.get('/wishlist')
    assert response.status_code == 200
    assert b"Wishlist" in response.data

# Test for reviews route
def test_reviews(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.get('/reviews')
    assert response.status_code == 200
    assert b"Reviews" in response.data

# Test for add book route
def test_add_book(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.post('/add_book/library', data={'title': 'Test Book', 'author': 'Test Author'})
    assert response.status_code == 302
    assert response.location == "/library"

# Test for delete book route
def test_delete_book(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.post('/delete_book/library', data={'book_id': '1'})
    assert response.status_code == 302
    assert response.location == "/library"

# Test for update book route
def test_update_book(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.post('/update_book', data={'book_id': '1', 'title': 'Updated Book'})
    assert response.status_code == 302
    assert response.location == "/library"

# Test for new password route
def test_new_password(test_client, test_user):
    test_client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.post('/new_password', data={'password': 'newpassword', 'confirmation': 'newpassword'})
    assert response.status_code == 302
    assert response.location == "/login"