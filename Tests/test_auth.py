# test_auth.py
import pytest

from flask_server.website import create_app, db
from flask_server.website.authorization.model import Users
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()
@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    user = Users(login='testuser', password=generate_password_hash('test'), user_type='student', email='test@test.com', phone_nr='123456789', photo = "abc", logged_in = False)
    db.session.add(user)
    db.session.commit()

    yield db

    db.drop_all()

    """
def test_successful_login(test_client, init_database):

    response = test_client.post('/login', data=dict(username='testuser', password='test'), follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    assert b'Logged in!' in response.data # Sprawdź czy użytkownik otrzymuje komunikat o sukcesie
    """

def test_incorrect_login(test_client, init_database):
    response = test_client.post('/login', data=dict(username='testuser', password='wrongpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Incorrect password!' in response.data # Sprawdź czy użytkownik otrzymuje komunikat o błędzie

def test_nonexistent_user(test_client, init_database):
    response = test_client.post('/login', data=dict(username='nonexistent', password='test'), follow_redirects=True)
    assert response.status_code == 200
    assert b'User not found!' in response.data # Sprawdź czy użytkownik otrzymuje komunikat o błędzie