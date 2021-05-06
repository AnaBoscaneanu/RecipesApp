# Configure fixtures for the tests

import pytest
from app_files.models import Users, db
from app_files.webapp import getApp

from werkzeug.security import check_password_hash, generate_password_hash

@pytest.fixture(scope='module')
def new_user():
    user = Users('random', 'FlaskIsAwesome')
    return user

@pytest.fixture(scope='module')
def test_client():
    flask_app = getApp()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client 

@pytest.fixture(scope='module')
def init_database(test_client):

    # Insert user data in table Users
    user1 = Users(username='John Doe', hash=generate_password_hash('MyPassword', method='pbkdf2:sha256', salt_length=8))
    db.session.add(user1)
    db.session.commit()

    yield # this is where the testing happens!

    record = db.session.query(Users).filter_by(username='John Doe').first()
    db.session.delete(record)
    db.session.commit()
