from flask import request

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

# def test_valid_registration(test_client, init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/register' page is posted to (POST)
#     THEN check the response is valid and the user is logged in
#     """
#     response = test_client.post('/register', data = dict(username='NewName', password='NewPassword', confirmation='NewPassword'))
#     assert response.status_code == 302
#     assert b'Your passwords do not match' not in response.data

