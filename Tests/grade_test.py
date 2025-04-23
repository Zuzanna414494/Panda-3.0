import pytest
from flask_server.website import create_app, db
from flask_server.website.authorization.model import Students, Subjects, Teachers
from flask_server.website.grades.model import Grades
from flask_server.website.authorization.model import Users
from werkzeug.security import generate_password_hash
from datetime import datetime

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
    teacher_user = Users(login='teacher_user', password=generate_password_hash('password'), user_type='teacher', email='teacher@example.com', phone_nr=123456789, photo = "abc", logged_in = False)
    db.session.add(teacher_user)
    db.session.commit()

    teacher = Teachers(teacher_id=teacher_user.user_id, name='John', surname='Doe', classroom_nr=101, description='Math Teacher')
    db.session.add(teacher)
    db.session.commit()

    subject = Subjects(subject_name='Math', class_name='3A', teacher_id=teacher.teacher_id)
    db.session.add(subject)
    db.session.commit()

    student_user = Users(login='student_user', password=generate_password_hash('password'), user_type='student', email='student@example.com', phone_nr=123456789, photo = "abc", logged_in = False)
    db.session.add(student_user)
    db.session.commit()

    student = Students(student_id=student_user.user_id, name='Jane', surname='Doe', gradebook_nr=123, class_name='3A', date_of_birth=datetime.now(), place_of_birth='City', address='Street 1')
    db.session.add(student)
    db.session.commit()



    yield db

    db.session.remove()
    db.drop_all()

def test_add_grade(test_client, init_database):
    subject = Subjects.query.first()
    student = Students.query.first()

    new_grade = Grades(subject_id=subject.subject_id, type=3, weight=1, student_id=student.student_id, description='Test Grade', is_final=False)
    db.session.add(new_grade)
    db.session.commit()

    added_grade = Grades.query.filter_by(description='Test Grade').first()
    assert added_grade is not None
    assert added_grade.subject_id == subject.subject_id
    assert added_grade.student_id == student.student_id

def test_delete_grade(test_client, init_database):
    new_grade = Grades(subject_id=1, type=1, weight=1, student_id=1, description="Test Grade2", is_final=False)
    db.session.add(new_grade)
    db.session.commit()

    grade = Grades.query.filter_by(description="Test Grade2").first()
    assert grade is not None

    db.session.delete(grade)
    db.session.commit()

    deleted_grade = Grades.query.filter_by(description="Test Grade2").first()
    assert deleted_grade is None

'''
def login_user(test_client, username, password):
    return test_client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def test_add_grade_functional(test_client, init_database):
    # Symulacja logowania (zakładając, że istnieje odpowiednia funkcja logowania)
    login_user(test_client, 'teacher_user', 'password')

    print(login_user)

    # Symulacja wysłania formularza dodawania oceny
    response = test_client.post('/grades/3A', data={
        "subject_id": 1,
        "type": 5,
        "weight": 1,
        "student_id": 1,
        "description": "Test Grade66",
        "is_final": False
    }, follow_redirects=True)


    print (response)

    # Sprawdzenie, czy strona zawiera informacje o dodanej ocenie
    #assert b'Test Grade' in response.data
    #assert b'Grade added!' in response.data

def test_delete_grade_functional(test_client, init_database):
    # Symulacja logowania
    login(test_client)

    # Najpierw dodajemy ocenę, którą potem usuniemy
    test_add_grade(test_client, init_database)

    # Symulacja usunięcia oceny
    response = test_client.post('/grades/3A', data={
        "delete": True,
        "grade_id_delete": 1  # Zakładamy, że ID dodanej oceny to 1
    }, follow_redirects=True)

    # Sprawdzenie, czy strona nie zawiera już usuniętej oceny
    assert b'Test Grade' not in response.data
    assert b'Grade deleted!' in response.data
'''
