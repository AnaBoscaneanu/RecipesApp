from app_files.models import Users

def test_new_user(new_user):
    """
    GIVEN a Users model
    WHEN a new User is created
    THEN check username, hash are defined correctly
    """
    
    assert new_user.username == 'random'
    assert new_user.hash == 'FlaskIsAwesome'


