import pytest
from flask_server.website import create_app, db
from flask_server.website.authorization.model import Users
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='module')
def test_app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_create_user(test_app):
    with test_app.app_context():
        new_user = Users(login='testuser', password=generate_password_hash('test'), user_type='student', email='test@test.com', phone_nr='123456789', photo = "abc", logged_in = False)
        db.session.add(new_user)
        db.session.commit()

        user = Users.query.filter_by(login='testuser').first()
        assert user is not None
        assert user.login == 'testuser'
        assert user.user_type == 'student'
