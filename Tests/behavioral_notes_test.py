import pytest
from flask_server.website import create_app, db
from flask_server.website.authorization.model import Students, Teachers, Users
from flask_server.website.timetable.model import Subjects
from flask_server.website.behavioral_notes.model import BehavioralNotes
from werkzeug.security import generate_password_hash
from datetime import datetime, date


@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')
    testing_client = app.test_client()

    with app.app_context():
        db.create_all()
        yield testing_client
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def init_database():
    # Tworzenie użytkownika nauczyciela
    teacher_user = Users(login='teacher_user', password=generate_password_hash('password'),
                         user_type='teacher', email='teacher@example.com', phone_nr=123456789,
                         photo="abc", logged_in=False)
    db.session.add(teacher_user)
    db.session.commit()

    # Tworzenie nauczyciela
    teacher = Teachers(teacher_id=teacher_user.user_id, name='John', surname='Doe',
                       classroom_nr=101, description='Math Teacher')
    db.session.add(teacher)
    db.session.commit()

    # Tworzenie przedmiotu
    subject = Subjects(subject_name='Math', class_name='3A', teacher_id=teacher.teacher_id)
    db.session.add(subject)
    db.session.commit()

    # Tworzenie użytkownika ucznia
    student_user = Users(login='student_user', password=generate_password_hash('password'),
                         user_type='student', email='student@example.com', phone_nr=123456789,
                         photo="abc", logged_in=False)
    db.session.add(student_user)
    db.session.commit()

    # Tworzenie ucznia
    student = Students(student_id=student_user.user_id, name='Jane', surname='Doe',
                      gradebook_nr=123, class_name='3A', date_of_birth=datetime.now().date(),
                      place_of_birth='City', address='Street 1')
    db.session.add(student)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()


def test_add_behavioral_note(test_client, init_database):
    """Test dodawania nowej notatki behawioralnej."""

    student = Students.query.first()
    teacher = Teachers.query.first()
    subject = Subjects.query.first()

    new_note = BehavioralNotes(
        student_id=student.student_id,
        teacher_id=teacher.teacher_id,
        subject_id=subject.subject_id,
        behavior_type='negative',
        category='discipline',
        title='Bad behavior',
        description='Student was disruptive during class.',
        behavior_score=2,
        incident_date=date.today(),
        parent_notified=False,
        requires_followup=True
    )

    db.session.add(new_note)
    db.session.commit()

    added_note = BehavioralNotes.query.filter_by(title='Bad behavior').first()
    assert added_note is not None
    assert added_note.student_id == student.student_id
    assert added_note.teacher_id == teacher.teacher_id
    assert added_note.subject_id == subject.subject_id


def test_edit_behavioral_note(test_client, init_database):
    """Test edycji istniejącej notatki behawioralnej."""

    # Najpierw dodaj notatkę
    student = Students.query.first()
    teacher = Teachers.query.first()
    subject = Subjects.query.first()

    new_note = BehavioralNotes(
        student_id=student.student_id,
        teacher_id=teacher.teacher_id,
        subject_id=subject.subject_id,
        behavior_type='negative',
        category='discipline',
        title='Bad behavior',
        description='Student was disruptive during class.',
        behavior_score=2,
        incident_date=date.today(),
        parent_notified=False,
        requires_followup=True
    )
    db.session.add(new_note)
    db.session.commit()

    # Pobierz dodaną notatkę
    note_to_edit = BehavioralNotes.query.filter_by(title='Bad behavior').first()

    # Edytuj notatkę
    note_to_edit.description = 'Student was talking during the lesson.'
    note_to_edit.behavior_score = 1
    db.session.commit()

    # Sprawdź, czy zmiany zostały zapisane
    edited_note = BehavioralNotes.query.get(note_to_edit.note_id)
    assert edited_note.description == 'Student was talking during the lesson.'
    assert edited_note.behavior_score == 1


def test_delete_behavioral_note(test_client, init_database):
    """Test usuwania notatki behawioralnej."""

    # Najpierw dodaj notatkę
    student = Students.query.first()
    teacher = Teachers.query.first()
    subject = Subjects.query.first()

    new_note = BehavioralNotes(
        student_id=student.student_id,
        teacher_id=teacher.teacher_id,
        subject_id=subject.subject_id,
        behavior_type='negative',
        category='discipline',
        title='Bad behavior',
        description='Student was disruptive during class.',
        behavior_score=2,
        incident_date=date.today(),
        parent_notified=False,
        requires_followup=True
    )
    db.session.add(new_note)
    db.session.commit()

    # Pobierz dodaną notatkę
    note_to_delete = BehavioralNotes.query.filter_by(title='Bad behavior').first()

    # Usuń notatkę
    db.session.delete(note_to_delete)
    db.session.commit()

    # Sprawdź, czy notatka została usunięta
    deleted_note = BehavioralNotes.query.get(note_to_delete.note_id)
    assert deleted_note is None


def login_user(test_client, username, password):
    """Funkcja pomocnicza do symulacji logowania."""
    return test_client.post('/authorization/login', data=dict(
        login=username,
        password=password
    ), follow_redirects=True)


def test_add_behavioral_note_functional(test_client, init_database):
    """Test funkcjonalny dodawania notatki (wymaga logowania)."""

    # Symuluj logowanie nauczyciela
    login_user(test_client, 'teacher_user', 'password')

    # Symuluj wysłanie formularza dodawania notatki
    response = test_client.post('/behavioral_notes/3A', data={
        "add": True,
        "student_id": 1,
        "subject_id": 1,
        "behavior_type": "negative",
        "category": "discipline",
        "title": "Fighting",
        "description": "Student got into a fight with another student",
        "behavior_score": 1,
        "incident_date": date.today().strftime('%Y-%m-%d'),
        "parent_notified": False,
        "requires_followup": True
    }, follow_redirects=True)

    # Sprawdź, czy dodanie się powiodło (sprawdź status kodu i komunikaty)
    assert response.status_code == 200  # Lub inny oczekiwany kod
    assert b'Note added successfully!' in response.data


def test_edit_behavioral_note_functional(test_client, init_database):
    """Test funkcjonalny edycji notatki."""

    # Symuluj logowanie
    login_user(test_client, 'teacher_user', 'password')

    # Najpierw dodaj notatkę
    test_add_behavioral_note_functional(test_client, init_database)

    # Symuluj edycję notatki
    response = test_client.post('/behavioral_notes/3A', data={
        "edit": True,
        "note_id": 1,  # Załóżmy, że ID dodanej notatki to 1
        "student_id": 1,
        "subject_id": 1,
        "behavior_type": "negative",
        "category": "discipline",
        "title": "Fighting",
        "description": "Student got into a fight with another student. Apologies were exchanged.",
        "behavior_score": 1,
        "incident_date": date.today().strftime('%Y-%m-%d'),
        "parent_notified": False,
        "requires_followup": True
    }, follow_redirects=True)

    # Sprawdź, czy edycja się powiodła
    assert response.status_code == 200
    assert b'Note updated successfully!' in response.data


def test_delete_behavioral_note_functional(test_client, init_database):
    """Test funkcjonalny usuwania notatki."""

    # Symuluj logowanie
    login_user(test_client, 'teacher_user', 'password')

    # Najpierw dodaj notatkę
    test_add_behavioral_note_functional(test_client, init_database)

    # Symuluj usunięcie notatki
    response = test_client.post('/behavioral_notes/3A', data={
        "delete": True,
        "note_id_delete": 1  # Załóżmy, że ID dodanej notatki to 1
    }, follow_redirects=True)

    # Sprawdź, czy usunięcie się powiodło
    assert response.status_code == 200
    assert b'Note deleted successfully!' in response.data