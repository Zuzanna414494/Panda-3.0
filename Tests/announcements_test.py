import pytest
from flask_server.website import create_app, db
from flask_server.website.models import Users, Announcements
from werkzeug.security import generate_password_hash
from datetime import datetime

@pytest.fixture(scope='module')
def test_app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture(scope='module')
def init_database(test_app):
    user = Users(login='testuser', password=generate_password_hash('test'), user_type='teacher', email='test@test.com', phone_nr='123456789', photo = "abc", logged_in = False)
    db.session.add(user)
    db.session.commit()

def test_add_announcement(test_app, init_database):
    with test_app.app_context():
        new_announcement = Announcements(
            description='Test Announcement',
            add_date=datetime.now(),
            in_archive=False,
            teacher_id=1
        )
        db.session.add(new_announcement)
        db.session.commit()

        announcement = Announcements.query.filter_by(description='Test Announcement').first()
        assert announcement is not None
        assert announcement.description == 'Test Announcement'
