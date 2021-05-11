from flask import request
from app_files.models import Users, db
import pytest

def test_login_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is required (GET)
    THEN check the response is valid
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'HOME' in response.data
    assert b'Sign In' in response.data
    assert b'Register' not in response.data

def test_valid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login', data = dict(username='John Doe', password='MyPassword'))
    assert response.status_code == 302
    assert request.form.get("username") == 'John Doe'
    assert request.form.get("password") == 'MyPassword'
    assert b'The username or the password is incorrect.' not in response.data


def test_invalid_login(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST) with invalid credentials
    THEN check an error message is returned to the user
    """
    response = test_client.post('/login', data = dict(username='MyName', password='NotMyPassword'))
    assert response.status_code == 200
    assert request.form.get("username") == 'MyName'
    assert request.form.get("password") == 'NotMyPassword'   
    assert b'The username or the password is incorrect.' in response.data

def test_valid_registration(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST)
    THEN check the response is valid and the user is logged in
    """
    response = test_client.post('/register', data = dict(username='NewName', password='NewPassword', confirmation='NewPassword'))    
    assert response.status_code == 302
    assert b'Your passwords do not match' not in response.data
    assert db.session.query(Users).filter_by(username='NewName').count() == 1
    
    # remove the new record from the database
    record = db.session.query(Users).filter_by(username='NewName').first()
    db.session.delete(record)
    db.session.commit()

@pytest.mark.parametrize('credentials',
[
    dict(username='NewName', password='NewPassword', confirmation='NotNewPassword'),
    dict(username='John Doe', password='NewPassword', confirmation='NewPassword')
])
def test_invalid_registration(test_client, credentials):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is posted to (POST) with invalid credentials(username already exists or passwords do not match)
    THEN check the new user was not registered in the database
    """
    response = test_client.post('/register', data = credentials)
    assert db.session.query(Users).filter_by(username='NewName').count() == 0
    assert db.session.query(Users).filter_by(username='John Doe').count() == 1
