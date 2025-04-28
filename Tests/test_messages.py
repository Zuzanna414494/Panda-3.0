import pytest
from flask_server.website import create_app, db
from flask_server.website.messages.model import Messages
from flask_server.website.authorization.model import Users
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
    with test_app.app_context():
        # Tworzymy dwóch użytkowników: nadawcę i odbiorcę
        sender = Users(login='sender', password=generate_password_hash('test'), user_type='teacher',
                       email='sender@test.com', phone_nr=111111111, photo="sender.jpg", logged_in=False)
        receiver = Users(login='receiver', password=generate_password_hash('test'), user_type='student',
                         email='receiver@test.com', phone_nr=222222222, photo="receiver.jpg", logged_in=False)
        db.session.add(sender)
        db.session.add(receiver)
        db.session.commit()


def test_add_message(test_app, init_database):
    with test_app.app_context():
        # Tworzymy nową wiadomość
        new_message = Messages(
            sender_id=1,
            receiver_id=2,
            subject='Test Subject',
            body='Test message body',
            send_date=datetime.now(),
            forwarded=False
        )
        db.session.add(new_message)
        db.session.commit()

        # Wyszukujemy wiadomość po temacie
        message = Messages.query.filter_by(subject='Test Subject').first()
        assert message is not None
        assert message.subject == 'Test Subject'
        assert message.body == 'Test message body'
        assert message.sender_id == 1
        assert message.receiver_id == 2
